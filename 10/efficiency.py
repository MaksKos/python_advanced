# pylint: disable=missing-docstring

import time
import json

import ujson

import cjson

def main():
    
    with open('dump.json') as f:
        json_str = json.load(f)

    print("\nTest dumps:\n")

    t_start = time.time()*1e3
    json_doc = json.dumps(json_str)
    t_stop = time.time()*1e3
    print(f'\t json: {t_stop-t_start} ms')

    t_start = time.time()*1e3
    ujson_doc = ujson.dumps(json_str)
    t_stop = time.time()*1e3
    print(f'\t ujson: {t_stop-t_start} ms')

    t_start = time.time()*1e3
    cjson_doc = cjson.dumps(json_str)
    t_stop = time.time()*1e3
    print(f'\t cjson: {t_stop-t_start} ms')

    print("\n Test loads:\n")

    t_start = time.time()*1e3
    json_doc = json.loads(json_doc)
    t_stop = time.time()*1e3
    print(f'\t json: {t_stop-t_start} ms')

    t_start = time.time()*1e3
    ujson_doc = ujson.loads(ujson_doc)
    t_stop = time.time()*1e3
    print(f'\t ujson: {t_stop-t_start} ms')

    t_start = time.time()*1e3
    cjson_doc = cjson.loads(cjson_doc)
    t_stop = time.time()*1e3
    print(f'\t cjson: {t_stop-t_start} ms\n')

if __name__ == "__main__":
    main()