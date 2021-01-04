# exactly_once.py

from kafka import KafkaConsumer, ConsumerRebalanceListener

# do not provide a topic when instantiating the consumer
consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9093'],
    group_id='group-1',
    enable_auto_commit=False,
)

# stand in for database
database = {} #DB()


class SaveOffsetsRebalanceListener(ConsumerRebalanceListener):

    def __init__(self, consumer):
        self.consumer = consumer

    def on_partitions_revoked(self, revoked):
        # here commit the current open db transaction if possible to avoid having to reprocess the current
        # un-persisted but processed batch messages -- not 100% necessary
        database.commit_transaction()

    def on_partitions_assigned(self, assigned):
        # on a rebalancing of partitions this method will be called if a new partition is assigned to this consumer
        for topic_partition in assigned:
            self.consumer.seek(topic_partition.partition, database.get_offset(topic_partition.partition))


def consume_messages():
    # subscribe to the topic we want to consume
    consumer.subscribe(['new_topic'], listener=SaveOffsetsRebalanceListener(consumer))
    # poll once to ensure joining of consumer group and partitions assigned
    consumer.poll(0)

    # seek to the offsets stored in the DB
    for topic_partition in consumer.assignment():
        # we use the offsets stored in our database rather than kafka
        offset = database.get_offset(topic_partition.partition)
        consumer.seek(topic_partition.partition, offset)

    while True:
        message_batch = consumer.poll()

        # enter DB transaction for batch
        with database.transaction():
            for topic_partition, partition_batch in message_batch.items():
                for message in partition_batch:
                    print(message.value.decode('utf-8'))
                    database.store_message(message.value)
                    database.store_offset(topic_partition.partition, message.offset)
        # commit of DB transaction on exit of context manager


if __name__ == '__main__':
    consume_messages()