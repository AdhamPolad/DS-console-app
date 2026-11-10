"""Topic 1: static array vs dynamic array (with benchmark)."""
from utils import measure, print_table


class ArrayBase:
    """Shared array logic. Subclasses decide what happens when full."""

    def __init__(self, capacity):
        self._data = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    def _ensure_space(self):
        raise NotImplementedError

    def insert(self, index, value):
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        self._ensure_space()
        for i in range(self._size, index, -1):      # shift right
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def append(self, value):
        self.insert(self._size, value)

    def delete_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        value = self._data[index]
        for i in range(index, self._size - 1):      # shift left
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        self._after_delete()
        return value

    def _after_delete(self):
        pass

    def search(self, value):
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    # uniform names used by the benchmark
    def insert_begin(self, v): self.insert(0, v)
    def delete_begin(self): return self.delete_at(0)
    def delete_end(self): return self.delete_at(self._size - 1)


class StaticArray(ArrayBase):
    """Fixed capacity: raises OverflowError when full."""

    def _ensure_space(self):
        if self._size == len(self._data):
            raise OverflowError("static array is full")


class DynamicArray(ArrayBase):
    """Doubles capacity when full, halves when 1/4 used."""

    def __init__(self, capacity=4):
        super().__init__(capacity)

    def _resize(self, new_cap):
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data

    def _ensure_space(self):
        if self._size == len(self._data):
            self._resize(len(self._data) * 2)

    def _after_delete(self):
        cap = len(self._data)
        if cap > 4 and self._size <= cap // 4:
            self._resize(cap // 2)


class PyList:
    """Wrapper around Python's built-in list (itself a dynamic array)."""

    def __init__(self):
        self.l = []

    def append(self, v): self.l.append(v)
    def insert_begin(self, v): self.l.insert(0, v)
    def delete_begin(self): return self.l.pop(0)
    def delete_end(self): return self.l.pop()
    def search(self, v): return self.l.index(v) if v in self.l else -1


def array_benchmark():
    sizes = [1000, 5000, 10000]
    reps = 100
    ops = ["Insert at end", "Insert at beginning", "Delete from beginning",
           "Delete from end", "Search (not found, worst case)"]
    results = {op: {"Static Array": [], "Dynamic Array": [], "Python list": []} for op in ops}

    for n in sizes:
        makers = {
            "Static Array": lambda: StaticArray(n + 3 * reps),
            "Dynamic Array": lambda: DynamicArray(),
            "Python list": lambda: PyList(),
        }
        for name, make in makers.items():
            arr = make()
            for i in range(n):
                arr.append(i)
            results[ops[0]][name].append(measure(lambda: arr.append(0), reps))
            results[ops[1]][name].append(measure(lambda: arr.insert_begin(0), reps))
            results[ops[2]][name].append(measure(lambda: arr.delete_begin(), reps))
            results[ops[3]][name].append(measure(lambda: arr.delete_end(), reps))
            results[ops[4]][name].append(measure(lambda: arr.search(-1), reps))

    print("\nRunning benchmark... (takes a few seconds)")
    print_table("ARRAY vs DYNAMIC ARRAY", sizes, results)
    print("""
Analysis:
 - Insert/delete at the beginning is O(n) for all arrays (elements must shift).
 - Insert at the end is O(1) for arrays (amortized O(1) for dynamic array,
   because of occasional resize/copy).
 - Search is O(n) (linear search) - time grows linearly with n.
 - Static array is fast but has a fixed size; dynamic array grows automatically.
 - Python list is much faster because it is implemented in C.""")
