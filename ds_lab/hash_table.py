"""Topic 4: hash table with separate chaining (contact book)."""
import random
from utils import measure


class HashTable:
    """Own hash table. Each bucket is a list (chain) of [key, value] pairs.
    Resizes (rehash) when load factor > 0.75."""

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0
        self.collisions = 0          # inserts into an already non-empty bucket

    def _hash(self, key):
        h = 0
        for ch in str(key):          # polynomial rolling hash
            h = (h * 31 + ord(ch)) % 1_000_000_007
        return h % self.capacity

    def put(self, key, value):
        bucket = self.buckets[self._hash(key)]
        for pair in bucket:
            if pair[0] == key:       # update existing key
                pair[1] = value
                return
        if bucket:
            self.collisions += 1
        bucket.append([key, value])
        self.size += 1
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key):
        for k, v in self.buckets[self._hash(key)]:
            if k == key:
                return v
        return None

    def remove(self, key):
        bucket = self.buckets[self._hash(key)]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self):
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collisions = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)

    def items(self):
        return [(k, v) for b in self.buckets for k, v in b]

    def stats(self):
        longest = max(len(b) for b in self.buckets)
        used = sum(1 for b in self.buckets if b)
        return (f"size={self.size}, buckets={self.capacity}, used buckets={used}, "
                f"load factor={self.size / self.capacity:.2f}, "
                f"longest chain={longest}, collisions={self.collisions}")

    def show_buckets(self):
        for i, b in enumerate(self.buckets):
            if b:
                print(f"  [{i:>3}] " + " -> ".join(f"{k}:{v}" for k, v in b))


def contact_book():
    print("\n--- Contact Book (Hash Table with chaining) ---")
    print("Commands: add <name> <phone> | find <name> | delete <name> | list | buckets | stats | back")
    ht = HashTable()
    while True:
        parts = input("contacts> ").strip().split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "back":
            return
        elif cmd == "add" and len(parts) >= 3:
            ht.put(parts[1], parts[2])
            print("Saved.")
        elif cmd == "find" and len(parts) >= 2:
            r = ht.get(parts[1])
            print(r if r else "Not found.")
        elif cmd == "delete" and len(parts) >= 2:
            print("Deleted." if ht.remove(parts[1]) else "Not found.")
        elif cmd == "list":
            for k, v in ht.items():
                print(f"  {k}: {v}")
        elif cmd == "buckets":
            ht.show_buckets()
        elif cmd == "stats":
            print(ht.stats())
        else:
            print("Unknown command or missing argument.")


def hash_table_demo():
    print("\n--- Hash Table demo: 5000 random keys ---")
    ht = HashTable()
    keys = [f"user{random.randint(0, 10**6)}" for _ in range(5000)]
    for k in keys:
        ht.put(k, 1)
    print(ht.stats())
    t_ht = measure(lambda: ht.get(random.choice(keys)), 2000)
    lst = list(set(keys))
    t_list = measure(lambda: random.choice(keys) in lst, 200)
    print(f"Hash table lookup : {t_ht:.2f} us (average O(1))")
    print(f"List linear search: {t_list:.2f} us (O(n))")
