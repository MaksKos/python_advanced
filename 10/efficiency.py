# pylint: disable=missing-docstring

import time
import json
import os
import ujson

import cjson

LOOP = 10
NAME = 'new.json'


def middel_time(func, arg, loop=LOOP):
    total = 0
    for _ in range(loop):
        t_start = time.time()*1e3
        func(arg)
        t_stop = time.time()*1e3
        total += t_stop-t_start
    return total/loop


def main():

    size = os.path.getsize(NAME)

    print(f"\nFile '{NAME}' size: {size//2**20} Mb\n")

    with open(NAME) as file:
        json_dict = json.load(file)

    print(f"\nTest DUMPS middle time of {LOOP} loops\n")

    print(f'\t json: {middel_time(json.dumps, json_dict)} ms')

    print(f'\t ujson: {middel_time(ujson.dumps, json_dict)} ms')

    print(f'\t cjson: {middel_time(cjson.dumps, json_dict)} ms')

    with open(NAME) as file:
        json_doc = file.read()

    print(f"\nTest LOADS middle time of {LOOP} loops\n")

    print(f'\t json: {middel_time(json.loads, json_doc)} ms')

    print(f'\t ujson: {middel_time(ujson.loads, json_doc)} ms')

    print(f'\t ujson: {middel_time(cjson.loads, json_doc)} ms\n')


if __name__ == "__main__":
    main()
