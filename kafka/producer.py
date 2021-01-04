from time import sleep

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def produce_message(message: str):
    producer.send('newtopic', message.encode('utf-8'))
    # flush the message buffer to force message delivery to broker on each iteration
    producer.flush()


if __name__ == '__main__':

    counter = 0
    while True:
        produce_message(str(counter))
        print(f'produced_message: {counter}')
        sleep(1)
        counter += 1