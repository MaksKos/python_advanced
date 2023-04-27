# pylint: disable=missing-docstring

import socket
import argparse
import threading
import queue
import requests
import re
import json
import collections

HOST = 'localhost'
PORT = 8080
SIZE = 4096


class Worker(threading.Thread):

    count = 0

    def __init__(self, q, n_top) -> None:
        self.q = q
        self.size = n_top
        self._is_run = True
        super().__init__()

    def url_stat(self, url):
        req = requests.get(url, allow_redirects=False).text
        text = re.sub('<[^>]*>', '', req).split()
        count = collections.Counter(text)
        to_json = {key:value for key, value in count.most_common(self.size)}
        return json.dumps(to_json)
    
    def run(self) -> None:
        while self._is_run:
            sock = self.q.get()
            with sock as s:
                while True:
                    data = s.recv(4096)
                    if data:
                        res = self.url_stat(data.decode())
                        s.sendall(res.encode())
                        self.__class__.count += 1
                        print(f'{self.count} urls have done')
                    else:
                        self.q.task_done()
                        break


class Master(threading.Thread):

    def __init__(self, q) -> None:
        self.q = q
        self._is_run = True
        super().__init__()
    
    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((HOST, PORT))
            server_sock.listen(5)
            while self._is_run:
                client_sock, addr = server_sock.accept()
                print("client connected", addr)
                self.q.put(client_sock)


def main(workers: int, n_top: int):
    q = queue.Queue()  
    threads = [Worker(q, n_top) for _ in range(workers)]
    threads.append(Master(q))
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    q.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w')
    parser.add_argument('-k')
    args = parser.parse_args()
    print(f"{args.w=}, {args.k=}")
    main(int(args.w), int(args.k))
