# pylint: disable=missing-docstring

import logging
import argparse

loglru = logging.getLogger('loglru')

format_file = logging.Formatter("%(asctime)s\t%(levelname)s\t[file]\t%(message)s",
                                "%Y %b %d, %H:%M:%S")
format_stdout = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s",
                                  "%H:%M:%S")

hand_file = logging.FileHandler("cache.log", encoding='utf-8')
hand_file.setLevel(logging.DEBUG)
hand_file.setFormatter(format_file)

hand_std = logging.StreamHandler()
hand_std.setLevel(logging.WARNING)
hand_std.setFormatter(format_stdout)

loglru.setLevel(logging.DEBUG)
loglru.addHandler(hand_file)


class NodeInfoFilter(logging.Filter):

    def filter(self, record):
        "filter message with 'node' in it"
        return "node" not in record.msg


class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        loglru.debug('create new node with key <%s>', key)


class LRUCache:

    def __init__(self, limit=42):
        self.cache = dict()
        self.head = None
        self.tail = None
        self.limit = limit
        loglru.info('create lru with size %d', limit)

    def _appnode(self, new_node):
        loglru.debug('add node with key <%s>', new_node.key)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            node = self.head
            node.prev = new_node
            new_node.next = node
            self.head = new_node

    def _removenode(self, node):
        loglru.debug('remove node with key <%s>', node.key)
        node_next = node.next
        node_prev = node.prev
        if node is self.head and node is self.tail:
            self.head, self.tail = None, None
            return None
        if node is self.head:
            self.head = node_next
            node_next.prev = None
            return None
        if node is self.tail:
            self.tail = node_prev
            node_prev.next = None
            return None
        node_next.prev = node_prev
        node_prev.next = node_next
        return None

    def _move_to_head(self, node):
        loglru.debug('move to head node with key <%s>', node.key)
        self._removenode(node)
        self._appnode(node)

    def get(self, key):
        node = self.cache.get(key)
        if node is None:
            loglru.critical('get: key <%s> not found', key)
            return None
        loglru.info('get: key <%s> is found', key)
        self._move_to_head(node)
        return node.value

    def set(self, key, value):
        node = self.cache.get(key)
        if node is None:
            loglru.warning('set: add new key <%s>', key)
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._appnode(new_node)
        else:
            loglru.info('set: update key <%s>', key)
            node.value = value
            self._move_to_head(node)

        if len(self.cache) > self.limit:
            loglru.error('set: delete key <%s>', self.tail.key)
            self.cache.pop(self.tail.key)
            self._removenode(self.tail)


def main(std: bool, filt: bool):

    if filt:
        loglru.addFilter(NodeInfoFilter())
    if std:
        loglru.addHandler(hand_std)

    lru_cache = LRUCache(3)

    lru_cache.set("url1", "news site")
    lru_cache.set("url2", "messanger")
    lru_cache.get('url3')
    lru_cache.set('url3', 'google')
    lru_cache.get('url1')
    lru_cache.set('url4', 'wiki')
    lru_cache.set("url1", "old site")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action="store_true")
    parser.add_argument('-f', action="store_true")
    args = parser.parse_args()

    main(args.s, args.f)
