import time
import weakref


class RegularClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class SlotClass:
    __slots__ = ["name", "age"]

    def __init__(self, name, age):
        self.name = name
        self.age = age


class WeakRefClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._weakref = weakref.ref(self)

    def get_weakref(self):
        return self._weakref()


def measure_time():
    num_instances = 1_000_000

    print("Замеры времени создания классов на миллионе экземплярах")
    print()

    start_time = time.time()
    regular_objects = [RegularClass(f"Актер {i}", i) for i in range(num_instances)]
    end_time = time.time()
    print(f"Время создания обычного класса: {end_time - start_time:.5f} " f"секунд")

    start_time = time.time()
    slot_objects = [SlotClass(f"Актер {i}", i) for i in range(num_instances)]
    end_time = time.time()
    print(f"Время создания класса со слотами: {end_time - start_time:.5f} " f"секунд")

    start_time = time.time()
    weakref_objects = [WeakRefClass(f"Актер {i}", i) for i in range(num_instances)]
    end_time = time.time()
    print(
        f"Время создания класса со слабыми ссылками:"
        f" {end_time - start_time:.5f} секунд"
    )

    print()
    print("Замеры времени изменения классов")
    print()

    start_time = time.time()
    for obj in regular_objects:
        obj.name += "_updated"
        obj.age += 1
    end_time = time.time()
    print(
        f"Время изменения для обычного класса: {end_time - start_time:.5f} " f"секунд"
    )

    start_time = time.time()
    for obj in slot_objects:
        obj.name += "_updated"
        obj.age += 1
    end_time = time.time()
    print(
        f"Время изменения для класса со слотами: {end_time - start_time:.5f} " f"секунд"
    )

    start_time = time.time()
    for obj in weakref_objects:
        obj.name += "_updated"
        obj.age += 1
    end_time = time.time()
    print(
        f"Время изменения для класса со слабыми ссылками:"
        f" {end_time - start_time:.5f} секунд"
    )


measure_time()
