class ListNode:

    def __init__(self, value, key=None):
        self.val = value
        self.key = key
        self.next, self.prev = None, None


class DoubleLList:

    def __init__(self):
        self.head = None
        self._end = None
        self._length = 0

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, node):
        self._end = node

    def insert_node_at_beggining(self, node: ListNode):
        """
        Функция вставляет переданную вершину в начало двусвязного списка
        """

        if not self.head:
            self.head = node
            self.end = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

        self._length += 1

    def del_node(self, node):
        """
        Функция удаляет нужную вершину из двусвязного списка
        """
        if not self.head:
            return

        if self.head == node:
            self.head = node.next
            if not self.head:
                self.end = self.head
        elif self.end == node:
            self.end = self.end.prev
            if not self.end:
                self.head = self.end
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        self.length -= 1


class LRUCache:

    def __init__(self, capacity=42):
        self.hash_map = dict()
        self.capacity = capacity
        self.double_ll = DoubleLList()

    def _make_correct_order(self, node):
        self.double_ll.del_node(node)
        self.double_ll.insert_node_at_beggining(node)

    def get(self, key):
        if key not in self.hash_map:
            return None

        node = self.hash_map[key]
        self._make_correct_order(node)

        return node.val

    def set(self, key, value):
        if key in self.hash_map:
            node = self.hash_map[key]
            node.val = value
            self._make_correct_order(node)
            return None

        new_node = ListNode(value, key)
        self.hash_map[key] = new_node
        self.double_ll.insert_node_at_beggining(new_node)

        if self.double_ll.length > self.capacity:
            last_node = self.double_ll.end
            last_node_key = last_node.key
            self.hash_map.pop(last_node_key)
            self.double_ll.del_node(last_node)
