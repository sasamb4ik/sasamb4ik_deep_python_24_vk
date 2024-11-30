import argparse
import logging
import sys


class EvenWordsFilter(logging.Filter):
    def filter(self, record):
        return len(record.getMessage().split()) % 2 != 0


def setup_logging(log_to_stdout, apply_filter):
    handlers = [logging.FileHandler("cache.log", mode="w")]

    if log_to_stdout:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )

    if apply_filter:
        new_logger = logging.getLogger()
        new_logger.addFilter(EvenWordsFilter())


logger = logging.getLogger()

######################### копипаст LRU из 5 дз #############################


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
        pass

    def del_node(self, node):
        pass


######################### конец копипаста #############################


class LRUCache:
    def __init__(self, capacity=42):
        self.hash_map = {}
        self.capacity = capacity
        self.double_ll = DoubleLList()
        logger.debug("Инициализация LRU с capacity: %s", capacity)

    def _make_correct_order(self, node):
        logger.debug("Корректируем порядок ключа: %s", node.key)
        self.double_ll.del_node(node)
        self.double_ll.insert_node_at_beggining(node)

    def get(self, key):
        logger.debug("Попытка получить значение по ключу: %s", key)
        if key not in self.hash_map:
            logger.warning("Ключ %s не найден", key)
            return None

        node = self.hash_map[key]
        self._make_correct_order(node)

        logger.info("Извлекли значение %s по ключу: %s", node.val, key)
        return node.val

    def set(self, key, value):
        logger.debug(
            "Попытка установить ключ: %s со значением: %s", key, value
        )

        if key in self.hash_map:
            node = self.hash_map[key]
            node.val = value
            logger.info(
                "Обновление существующего ключа: %s новым значением: %s",
                key,
                value,
            )
            self._make_correct_order(node)
            return

        new_node = ListNode(value, key)
        self.hash_map[key] = new_node
        logger.info("Вставка нового ключа: %s со значением: %s", key, value)

        if self.double_ll.length >= self.capacity:
            last_node = self.double_ll.end
            last_node_key = last_node.key

            logger.warning(
                "Превышена capacity, удаляем самый редкий элемент: " "%s",
                last_node_key,
            )

            del self.hash_map[last_node_key]
            self.double_ll.del_node(last_node)

        self.double_ll.insert_node_at_beggining(new_node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s")
    parser.add_argument("-f")

    args = parser.parse_args()

    setup_logging(args.s, args.f)
