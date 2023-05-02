# pylint: disable=missing-docstring

import sys
from unittest import TestCase
from lru_cache import Node, LRUCache


class TestNodes(TestCase):

    def test_apphead_one(self):
        node = Node('key', 'value')
        lru = LRUCache()
        lru._appnode(node)
        self.assertIs(node, lru.head)
        self.assertIs(node, lru.tail)
        self.assertIsNone(node.next)
        self.assertIsNone(node.prev)

    def test_apphead_two(self):
        node1 = Node('key1', 'value1')
        node2 = Node('key2', 'value2')
        lru = LRUCache()
        lru._appnode(node1)
        lru._appnode(node2)
        self.assertIs(node2, lru.head)
        self.assertIs(node1, lru.tail)
        self.assertIsNone(node1.next)
        self.assertIsNone(node2.prev)
        self.assertIs(node2, node1.prev)
        self.assertIs(node1, node2.next)

    def test_remove_one(self):
        node = Node('key', 'value')
        lru = LRUCache()
        lru._appnode(node)
        self.assertEqual(sys.getrefcount(node), 4)
        lru._removenode(node)
        self.assertIsNone(lru.head)
        self.assertIsNone(lru.tail)
        self.assertEqual(sys.getrefcount(node), 2)

    def test_remove_head(self):
        node1 = Node('key1', 'value1')
        node2 = Node('key2', 'value2')
        lru = LRUCache()
        lru._appnode(node1)
        lru._appnode(node2)
        lru._removenode(node2)
        self.assertEqual(sys.getrefcount(node2), 2)
        self.assertIs(node1, lru.head)
        self.assertIs(node1, lru.tail)
        self.assertIsNone(node1.next)
        self.assertIsNone(node1.prev)

    def test_remove_tail(self):
        node1 = Node('key1', 'value1')
        node2 = Node('key2', 'value2')
        lru = LRUCache()
        lru._appnode(node1)
        lru._appnode(node2)
        lru._removenode(node1)
        self.assertEqual(sys.getrefcount(node1), 2)
        self.assertIs(node2, lru.head)
        self.assertIs(node2, lru.tail)
        self.assertIsNone(node2.next)
        self.assertIsNone(node2.prev)

    def test_remove_middle(self):
        nodes = [Node('key'+str(i), 'val'+str(i)) for i in range(3)]
        lru = LRUCache()
        for node in nodes:
            lru._appnode(node)
        lru._removenode(nodes[1])
        self.assertEqual(sys.getrefcount(nodes[1]), 2)
        self.assertIs(nodes[2], lru.head)
        self.assertIs(nodes[0], lru.tail)
        self.assertIsNone(nodes[0].next)
        self.assertIsNone(nodes[2].prev)
        self.assertIs(nodes[2], nodes[0].prev)
        self.assertIs(nodes[0], nodes[2].next)

    def test_move_head(self):
        nodes = [Node('key'+str(i), 'val'+str(i)) for i in range(3)]
        lru = LRUCache()
        for node in nodes:
            lru._appnode(node)
        lru._move_to_head(nodes[2])
        new_order = iter([nodes[2], nodes[1], nodes[0]])
        node = lru.head
        while node.next is not None:
            self.assertIs(node, next(new_order))
            node = node.next

    def test_move_tail(self):
        nodes = [Node('key'+str(i), 'val'+str(i)) for i in range(3)]
        lru = LRUCache()
        for node in nodes:
            lru._appnode(node)
        lru._move_to_head(nodes[0])
        new_order = iter([nodes[0], nodes[2], nodes[1]])
        node = lru.head
        while node.next is not None:
            self.assertIs(node, next(new_order))
            node = node.next

    def test_move_mid(self):
        nodes = [Node('key'+str(i), 'val'+str(i)) for i in range(3)]
        lru = LRUCache()
        for node in nodes:
            lru._appnode(node)
        lru._move_to_head(nodes[1])
        new_order = iter([nodes[1], nodes[2], nodes[0]])
        node = lru.head
        while node.next is not None:
            self.assertIs(node, next(new_order))
            node = node.next


class TestLRU(TestCase):

    def test_lru(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.head.key, 'k2')  # addition test
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.head.key, 'k1')  # addition test

        cache.set("k3", "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k1"), "val1")

    def test_lru_single(self):
        cache = LRUCache(1)
        cache.set("k1", "val1")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "val2")

    def test_lru_update(self):
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k1", "new_val1")  # update
        self.assertEqual(len(cache.cache), 2)  # addition test
        self.assertEqual(cache.head.key, "k1")  # addition test
        cache.set("k3", "val3")
        cache.set("k4", "val4")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k4"), "val4")

    def test_none(self):
        cache = LRUCache(2)
        cache.set("k1", None)
        self.assertIsNone(cache.get("k1"))
        self.assertIsNotNone(cache.cache['k1'])  # node instance
