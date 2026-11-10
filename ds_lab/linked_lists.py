"""Topic 2: singly and doubly linked lists (with benchmark)."""
from utils import measure, print_table


class SNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """Head pointer only (classic textbook version)."""

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def prepend(self, value):                       # O(1)
        node = SNode(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def append(self, value):                        # O(n)
        node = SNode(value)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.size += 1

    def delete_first(self):                         # O(1)
        if not self.head:
            raise IndexError("list is empty")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value

    def delete_last(self):                          # O(n)
        if not self.head:
            raise IndexError("list is empty")
        if not self.head.next:
            return self.delete_first()
        cur = self.head
        while cur.next.next:
            cur = cur.next
        value = cur.next.value
        cur.next = None
        self.size -= 1
        return value

    def delete_value(self, value):                  # O(n)
        prev, cur = None, self.head
        while cur:
            if cur.value == value:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def search(self, value):                        # O(n)
        cur, i = self.head, 0
        while cur:
            if cur.value == value:
                return i
            cur, i = cur.next, i + 1
        return -1

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out


class DNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Head and tail pointers + prev links."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def prepend(self, value):                       # O(1)
        node = DNode(value)
        if self.head:
            node.next = self.head
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        self.size += 1

    def append(self, value):                        # O(1)
        node = DNode(value)
        if self.tail:
            node.prev = self.tail
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.size += 1

    def _unlink(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.size -= 1
        return node.value

    def delete_first(self):                         # O(1)
        if not self.head:
            raise IndexError("list is empty")
        return self._unlink(self.head)

    def delete_last(self):                          # O(1)
        if not self.tail:
            raise IndexError("list is empty")
        return self._unlink(self.tail)

    def delete_value(self, value):                  # O(n)
        cur = self.head
        while cur:
            if cur.value == value:
                self._unlink(cur)
                return True
            cur = cur.next
        return False

    def search(self, value):                        # O(n)
        cur, i = self.head, 0
        while cur:
            if cur.value == value:
                return i
            cur, i = cur.next, i + 1
        return -1

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def to_list_backward(self):                     # only possible in doubly list
        out, cur = [], self.tail
        while cur:
            out.append(cur.value)
            cur = cur.prev
        return out


def linked_list_benchmark():
    sizes = [1000, 5000, 10000]
    reps = 100
    ops = ["Insert at head", "Insert at tail", "Delete first", "Delete last",
           "Search (not found)"]
    results = {op: {"Singly LL": [], "Doubly LL": []} for op in ops}

    print("\nRunning benchmark... (takes a few seconds)")
    for n in sizes:
        for name, cls in (("Singly LL", SinglyLinkedList), ("Doubly LL", DoublyLinkedList)):
            lst = cls()
            for i in range(n):
                lst.prepend(i)
            results[ops[0]][name].append(measure(lambda: lst.prepend(0), reps))
            results[ops[1]][name].append(measure(lambda: lst.append(0), reps))
            results[ops[2]][name].append(measure(lambda: lst.delete_first(), reps))
            results[ops[3]][name].append(measure(lambda: lst.delete_last(), reps))
            results[ops[4]][name].append(measure(lambda: lst.search(-1), reps))
    print_table("SINGLY vs DOUBLY LINKED LIST", sizes, results)
    print("""
Analysis:
 - Insert/delete at head: O(1) in both.
 - Insert at tail and delete last: O(n) in singly (must walk the list),
   O(1) in doubly (tail pointer + prev link).
 - Search: O(n) in both.
 - Doubly list costs more memory (extra prev pointer) but allows backward traversal.""")


def linked_list_demo():
    s, d = SinglyLinkedList(), DoublyLinkedList()
    for x in (10, 20, 30, 40):
        s.append(x)
        d.append(x)
    s.prepend(5)
    d.prepend(5)
    print("\nSingly list :", s.to_list())
    print("Doubly list :", d.to_list())
    print("Doubly list backward:", d.to_list_backward())
    s.delete_value(20)
    d.delete_value(20)
    print("After deleting 20 ->", s.to_list(), d.to_list())
    print("Search 30 -> index", s.search(30), "/", d.search(30))
