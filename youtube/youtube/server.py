from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import subprocess
from urllib import parse
import os
import datetime


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _html(self, message):
        return message.encode("utf8")

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/crawl':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self._set_headers()
            params = parse.parse_qs(parse.urlsplit(str(post_data, 'utf-8')).path)
            if 'watch_id' not in params:
                out = 'watch_id is required.'
            else:
                out = self.run_craler(params['watch_id'][0])
        else:
            out = 'Not found!'
        self.wfile.write(bytes("{\'result\': '" + out + "'}", 'utf-8'))

    def run_craler(self, watch_id=''):
        if watch_id == '':
            return 'watch_id is required.'
        currentDT = datetime.datetime.now()
        out = ''
        if os.path.exists('/mnt'):
            csv_path = '/mnt/' + watch_id + '_' + currentDT.strftime("%Y%m%d%H%M%S") + '.csv'
        else:
            csv_path = '../' + watch_id + '_' + currentDT.strftime("%Y%m%d%H%M%S") + '.csv'
        process = subprocess.Popen(
            ['scrapy', 'crawl', 'youtube', '-a', 'watch_id=' + watch_id, '-o', csv_path],
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


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",  # localhost
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
