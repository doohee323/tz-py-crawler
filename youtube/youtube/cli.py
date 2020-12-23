import argparse
import subprocess
import glob
import os

APP_VERSION = '0.1'


class Cli:
    type = ''
    path = ''
    list = ''
    query = ''
    json_path = ''

    def do_GET(self):
        if '/crawl' in self.path:
            params = dict(x.split('=') for x in self.query.split('&'))
            if 'watch_ids' not in params:
                out = 'watch_ids is required.'
            else:
                out = self.run_craler(params['watch_ids'], 'GET')
        elif self.path == '/health':
            out = "{\'version\': '" + APP_VERSION + "'}"
        else:
            out = 'Not found!'
        print("{\'result\': '" + out + "'}")

    def do_POST(self):
        if self.path == '/crawl':
            post_data = ''
            files = glob.glob(self.list)
            if not files:
                return ''
            try:
                file = open(max(files, key=os.path.getctime), mode='r')
                post_data = file.read()
                file.close()
            except TypeError:
                pass
            params = post_data.split(',')
            if len(params) == 0:
                out = 'watch_ids is required.'
            else:
                if not os.path.exists(self.json_path):
                    os.makedirs(self.json_path)
                for watch_id in params:
                    out = self.run_craler(watch_id, 'POST')
                    try:
                        source_path = '/mnt/'
                        files = glob.glob(os.path.join(source_path, watch_id + '*.json'))
                        file = open(max(files, key=os.path.getctime), mode='r')
                        post_data = file.read()
                        file.close()
                        post_data = post_data.replace('\n', '').replace('},', '}\n')
                        post_data = post_data[1: len(post_data) - 1]
                        target_file = os.path.join(self.json_path, os.path.basename(file.name))
                        f2 = open(target_file, "a")
                        f2.write(post_data)
                        f2.close()
                        out = target_file
                    except Exception as e:
                        pass
        else:
            out = 'Not found!'
        print("{\'result\': '" + out + "'}")

    def run_craler(self, watch_ids='', exec_type='GET'):
        if watch_ids == '':
            return 'watch_ids is required.'
        out = ''
        if exec_type == 'POST':
            # curl -d "watch_ids=ioNng23DkIM" -X POST http://98.234.161.130:8000/crawl
            # curl -d "watch_ids=kVQEW0SNFqE" -X POST http://localhost:8000/crawl
            process = subprocess.Popen(
                ['curl', '-d', 'watch_ids=' + watch_ids, '-X', 'POST', self.domain + '/crawl'],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE,
                universal_newlines=True)
            while True:
                return_code = process.poll()
                if return_code is not None:
                    for out1 in process.stdout.readlines():
                        out = out + out1.strip()
                    break
            return out
        elif exec_type == 'GET':
            # curl http://98.234.161.130:8000/crawl?watch_ids=ioNng23DkIM
            # curl http://tz-py-crawler:8000/crawl?watch_ids=
            process = subprocess.Popen(
                ['curl', self.domain + '/crawl?watch_ids=' + watch_ids],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE,
                universal_newlines=True)
            while True:
                return_code = process.poll()
                if return_code is not None:
                    for out1 in process.stdout.readlines():
                        out = out + out1.strip()
                    break
            return out


def run(type="POST", domain="http://tz-py-crawler:8000", path="/crawl", list="/mnt/list.txt", query="", json_path="/mnt/result"):
    print(f"Starting with {type}, {path}, {list}, {query}")
    cli = Cli()
    cli.type = type
    cli.domain = domain
    cli.path = path
    cli.list = list
    cli.query = query
    cli.json_path = json_path
    if type == 'GET':
        cli.do_GET()
    elif type == 'POST':
        cli.do_POST()

# python youtube/youtube/cli.py -l /Volumes/workspace/etc/tz-k8s-vagrant/projects/tz-py-crawler/youtube/list.txt
# python3 youtube/youtube/cli.py -l /mnt/list.txt -d http://98.234.161.130:30007 -j /mnt/test
# python youtube/youtube/cli.py -t GET -q watch_ids=kVQEW0SNFqE
# python3 youtube/cli.py -l /mnt/list.txt -d http://98.234.161.130:30007 -j /mnt/result
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a CLI command.")
    parser.add_argument(
        "-t",
        "--type",
        default='POST',
        help="Specify request type (GET/POST)",
    )
    parser.add_argument(
        "-d",
        "--domain",
        default='http://tz-py-crawler:8000',
        help="Specify request domain",
    )
    parser.add_argument(
        "-p",
        "--path",
        default='/crawl',
        help="Specify request path",
    )
    parser.add_argument(
        "-l",
        "--list",
        default="/mnt/list.txt",
        help="Specify youtube_id list file path",
    )
    parser.add_argument(
        "-q",
        "--query",
        default="watch_ids=ioNng23DkIM",
        help="Specify youtube_id",
    )
    parser.add_argument(
        "-j",
        "--json_path",
        default="/mnt/result",
        help="Specify youtube_id",
    )
    args = parser.parse_args()
    run(type=args.type, domain=args.domain, path=args.path, list=args.list, query=args.query, json_path=args.json_path)
