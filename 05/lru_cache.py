# pylint: disable=missing-docstring

class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, limit=42):
        self.cache = dict()
        self.head = None
        self.tail = None
        self.limit = limit

    def _appnode(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            node = self.head
            node.prev = new_node
            new_node.next = node
            self.head = new_node

    def _removenode(self, node):
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
        self._removenode(node)
        self._appnode(node)

    def get(self, key):
        node = self.cache.get(key)
        if node is None:
            return None
        self._move_to_head(node)
        return node.value

    def set(self, key, value):
        node = self.cache.get(key)
        if node is None:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._appnode(new_node)
        else:
            node.value = value
            self._move_to_head(node)
        if len(self.cache) > self.limit:
            self.cache.pop(self.tail.key)
            self._removenode(self.tail)
