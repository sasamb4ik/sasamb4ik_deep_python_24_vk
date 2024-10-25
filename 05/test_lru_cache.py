import unittest

from lru_cache import ListNode, DoubleLList, LRUCache


class TestDoubleLList(unittest.TestCase):

    def setUp(self):
        self.dll = DoubleLList()

    def test_initial_length(self):
        self.assertEqual(self.dll.length, 0)

    def test_insert_node_at_begin(self):
        node1 = ListNode(10)
        self.dll.insert_node_at_beggining(node1)
        self.assertEqual(self.dll.length, 1)
        self.assertEqual(self.dll.head, node1)
        self.assertEqual(self.dll.end, node1)

        node2 = ListNode(20)
        self.dll.insert_node_at_beggining(node2)
        self.assertEqual(self.dll.length, 2)
        self.assertEqual(self.dll.head, node2)
        self.assertEqual(self.dll.end, node1)
        self.assertEqual(self.dll.head.next, node1)
        self.assertEqual(node1.prev, self.dll.head)

    def test_get_last_node(self):
        self.assertIsNone(self.dll.end)

        node1 = ListNode(10)
        self.dll.insert_node_at_beggining(node1)
        self.assertEqual(self.dll.end, node1)

        node2 = ListNode(20)
        self.dll.insert_node_at_beggining(node2)
        self.assertEqual(self.dll.end, node1)

    def test_del_node(self):
        node1 = ListNode(10)
        self.dll.del_node(node1)
        self.assertEqual(self.dll.length, 0)

        self.dll.insert_node_at_beggining(node1)
        self.dll.del_node(node1)
        self.assertEqual(self.dll.length, 0)
        self.assertIsNone(self.dll.head)
        self.assertIsNone(self.dll.end)

        node1 = ListNode(10)
        node2 = ListNode(20)
        self.dll.insert_node_at_beggining(node1)
        self.dll.insert_node_at_beggining(node2)

        self.dll.del_node(node2)
        self.assertEqual(self.dll.length, 1)
        self.assertEqual(self.dll.head, node1)
        self.assertEqual(self.dll.end, node1)

        self.dll.del_node(node1)
        self.assertEqual(self.dll.length, 0)
        self.assertIsNone(self.dll.head)
        self.assertIsNone(self.dll.end)


class TestLRUCache(unittest.TestCase):

    def setUp(self):
        self.capacity = 3
        self.cache = LRUCache(capacity=self.capacity)

    def test_initial_state(self):
        self.assertEqual(self.cache.capacity, self.capacity)
        self.assertEqual(len(self.cache.hash_map), 0)
        self.assertEqual(self.cache.double_ll.length, 0)
        self.assertIsNone(self.cache.double_ll.head)
        self.assertIsNone(self.cache.double_ll.end)

    def test_get_empty_cache(self):
        self.assertIsNone(self.cache.get(1))
        self.assertIsNone(self.cache.get("a"))
        self.assertIsNone(self.cache.get(None))

    def test_set_and_get(self):
        self.cache.set(1, "one")
        self.assertIn(1, self.cache.hash_map)
        self.assertEqual(self.cache.get(1), "one")

        self.cache.set(2, "two")
        self.assertIn(2, self.cache.hash_map)
        self.assertEqual(self.cache.get(2), "two")

        self.cache.set(3, "three")
        self.assertIn(3, self.cache.hash_map)
        self.assertEqual(self.cache.get(3), "three")

    def test_update_existing_key(self):
        self.cache.set(1, "one")
        self.assertEqual(self.cache.get(1), "one")

        self.cache.set(1, "uno")
        self.assertEqual(self.cache.get(1), "uno")
        self.assertEqual(self.cache.double_ll.length, 1)

    def test_capacity_exceeded(self):
        self.cache.set(1, "one")
        self.cache.set(2, "two")
        self.cache.set(3, "three")
        self.assertEqual(self.cache.double_ll.length, 3)

        self.cache.get(1)
        self.cache.get(3)

        self.cache.set(4, "four")
        self.assertEqual(len(self.cache.hash_map), self.capacity)
        self.assertNotIn(2, self.cache.hash_map)
        self.assertIn(1, self.cache.hash_map)
        self.assertIn(3, self.cache.hash_map)
        self.assertIn(4, self.cache.hash_map)

    def test_make_correct_order(self):
        self.cache.set(1, "one")
        self.cache.set(2, "two")
        self.cache.set(3, "three")

        self.cache.get(2)

        self.cache.set(4, "four")
        self.assertNotIn(1, self.cache.hash_map)
        self.assertIn(2, self.cache.hash_map)
        self.assertIn(3, self.cache.hash_map)
        self.assertIn(4, self.cache.hash_map)

        self.cache.set(1, "one")
        self.cache.set(2, "two")
        self.cache.set(3, "three")

        self.cache.get(1)
        self.cache.get(2)

        self.cache.set(4, "four")
        self.assertNotIn(3, self.cache.hash_map)

        self.cache.set(5, "five")
        self.assertNotIn(1, self.cache.hash_map)

        self.assertIn(2, self.cache.hash_map)
        self.assertIn(4, self.cache.hash_map)
        self.assertIn(5, self.cache.hash_map)

    def test_capacity_one(self):
        cache = LRUCache(capacity=1)
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)

        cache.set("b", 2)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)

    def overwriting_value(self):
        self.cache.set(1, "one")
        self.cache.set(2, "two")
        self.cache.set(3, "three")
        self.cache.set(2, "deux")

        self.assertEqual(self.cache.get(2), "deux")
        self.assertEqual(len(self.cache.hash_map), 3)
        self.assertEqual(self.cache.double_ll.length, 3)

    def test_large_number_of_operations(self):
        large_capacity = 1000
        large_cache = LRUCache(capacity=large_capacity)

        for i in range(large_capacity):
            large_cache.set(i, f"value_{i}")

        for i in range(large_capacity):
            self.assertEqual(large_cache.get(i), f"value_{i}")

        for i in range(large_capacity, large_capacity + 500):
            large_cache.set(i, f"value_{i}")

        self.assertEqual(large_cache.double_ll.length, large_capacity)
        for i in range(500):
            self.assertNotIn(i, large_cache.hash_map)

        for i in range(500, large_capacity + 500):
            self.assertIn(i, large_cache.hash_map)
