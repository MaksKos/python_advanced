# pylint: disable=missing-docstring

import socket
import argparse
import threading

HOST = 'localhost'
PORT = 8080
SIZE = 4096


def thread_socket(file, lock):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        while True:
            lock.acquire()
            line = file.readline()
            lock.release()
            if not line:
                break
            s.sendall(line.encode())
            data = s.recv(SIZE)
            print(f'{line}: {data.decode()}')


def main(n: int, file_name: str):
    with open(file_name) as file:
        lock = threading.Lock()
        threads = [
            threading.Thread(
                target=thread_socket,
                args=(file, lock),
            )
            for _ in range(n)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n_thr')
    parser.add_argument('file')
    args = parser.parse_args()
    main(int(args.n_thr), args.file)
