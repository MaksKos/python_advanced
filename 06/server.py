# pylint: disable=missing-docstring

import socket
import argparse
import threading
import queue
import re
import json
import collections
import requests

HOST = 'localhost'
PORT = 8080
SIZE = 4096


class Worker(threading.Thread):

    count = 0

    def __init__(self, que, n_top, lock) -> None:
        self.que = que
        self.size = n_top
        self.lock = lock
        self._is_run = True
        super().__init__()

    def url_stat(self, url):
        req = requests.get(url, allow_redirects=False).text
        text = re.sub('<[^>]*>', '', req).split()
        count = collections.Counter(text)
        to_json = dict(count.most_common(self.size))
        return json.dumps(to_json)

    def run(self) -> None:
        while self._is_run:
            new_sock = self.que.get()
            with new_sock as sock:
                try:
                    while True:
                        data = sock.recv(4096)
                        if data:
                            try:
                                res = self.url_stat(data.decode())
                            except requests.exceptions.RequestException as req_err: 
                                print(req_err)
                                sock.sendall("URL errro".encode())
                                continue

                            sock.sendall(res.encode())

                            self.lock.acquire()
                            self.__class__.count += 1
                            print(f'{self.count} urls have done')
                            self.lock.release()
                        else:
                            self.que.task_done()
                            break
                        
                except socket.error as error:
                    print(error.strerror)
                    continue


class Master(threading.Thread):

    def __init__(self, que) -> None:
        self.que = que
        self._is_run = True
        super().__init__()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((HOST, PORT))
            server_sock.listen(5)
            while self._is_run:
                try:
                    client_sock, addr = server_sock.accept()
                except socket.error as error:
                    print(error.strerror)
                    continue
                print("client connected", addr)
                self.que.put(client_sock)


def main(workers: int, n_top: int):
    que = queue.Queue()
    lock = threading.Lock()
    threads = [Worker(que, n_top, lock) for _ in range(workers)]
    threads.append(Master(que))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    que.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w')
    parser.add_argument('-k')
    args = parser.parse_args()
    print(f"{args.w=}, {args.k=}")
    main(int(args.w), int(args.k))
