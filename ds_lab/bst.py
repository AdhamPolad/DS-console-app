"""Topic 5: binary search tree."""
import random
import time


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key):
        if not self.root:
            self.root = TreeNode(key)
            self.size += 1
            return True
        cur = self.root
        while True:
            if key == cur.key:
                return False                      # no duplicates
            side = "left" if key < cur.key else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, TreeNode(key))
                self.size += 1
                return True
            cur = nxt

    def search(self, key):
        """Returns (found, number of comparisons)."""
        cur, comps = self.root, 0
        while cur:
            comps += 1
            if key == cur.key:
                return True, comps
            cur = cur.left if key < cur.key else cur.right
        return False, comps

    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self.size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return None, False
        if key < node.key:
            node.left, d = self._delete(node.left, key)
            return node, d
        if key > node.key:
            node.right, d = self._delete(node.right, key)
            return node, d
        # found
        if node.left is None:                     # case 1 & 2: 0 or 1 child
            return node.right, True
        if node.right is None:
            return node.left, True
        succ = node.right                          # case 3: two children
        while succ.left:                           # in-order successor
            succ = succ.left
        node.key = succ.key
        node.right, _ = self._delete(node.right, succ.key)
        return node, True

    def inorder(self):                             # iterative -> safe for deep trees
        out, stack, cur = [], [], self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            out.append(cur.key)
            cur = cur.right
        return out

    def height(self):                              # iterative
        if not self.root:
            return 0
        best, stack = 0, [(self.root, 1)]
        while stack:
            node, d = stack.pop()
            best = max(best, d)
            if node.left:
                stack.append((node.left, d + 1))
            if node.right:
                stack.append((node.right, d + 1))
        return best

    def show(self):
        if self.height() > 8:
            print("Tree too tall to draw (height > 8).")
            return
        def rec(node, level):
            if node:
                rec(node.right, level + 1)
                print("      " * level + str(node.key))
                rec(node.left, level + 1)
        print("(root is in the middle-left, right subtree on top)")
        rec(self.root, 0)


def bst_menu():
    print("\n--- Binary Search Tree ---")
    print("Commands: insert <n> | search <n> | delete <n> | inorder | show | height | back")
    t = BST()
    while True:
        parts = input("bst> ").strip().split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "back":
            return
        if cmd in ("insert", "search", "delete"):
            if len(parts) < 2 or not parts[1].lstrip("-").isdigit():
                print("Give an integer, e.g.  insert 15")
                continue
            n = int(parts[1])
            if cmd == "insert":
                print("Inserted." if t.insert(n) else "Already exists.")
            elif cmd == "search":
                found, c = t.search(n)
                print(f"{'Found' if found else 'Not found'} after {c} comparisons.")
            else:
                print("Deleted." if t.delete(n) else "Not found.")
        elif cmd == "inorder":
            print(t.inorder())
        elif cmd == "show":
            t.show()
        elif cmd == "height":
            print("Height:", t.height(), "| Size:", t.size)
        else:
            print("Unknown command.")


def bst_sorted_vs_random():
    n = 1000
    data = list(range(n))
    shuffled = data[:]
    random.shuffle(shuffled)

    print(f"\n--- BST: sorted vs random insertion (n={n}) ---")
    rows = []
    for name, seq in (("Sorted order", data), ("Random order", shuffled)):
        t = BST()
        start = time.perf_counter()
        for x in seq:
            t.insert(x)
        build = (time.perf_counter() - start) * 1000
        comps = [t.search(random.randint(0, n - 1))[1] for _ in range(500)]
        rows.append((name, t.height(), sum(comps) / len(comps), build))

    print(f"{'Insertion order':<16}{'Height':<10}{'Avg search comparisons':<26}{'Build time (ms)'}")
    for name, h, c, b in rows:
        print(f"{name:<16}{h:<10}{c:<26.1f}{b:.2f}")

    print("\nSmall example, inserting 1..7 in sorted order:")
    t = BST()
    for x in range(1, 8):
        t.insert(x)
    t.show()
    print("\nSmall example, inserting 4,2,6,1,3,5,7 (balanced order):")
    t = BST()
    for x in (4, 2, 6, 1, 3, 5, 7):
        t.insert(x)
    t.show()
    print("""
Explanation:
 - Sorted data makes every new key larger than the previous one, so it always
   goes to the RIGHT. The tree becomes a "linked list" (degenerate tree):
   height = n, and search/insert/delete become O(n).
 - Random data produces a bushy tree with height about log2(n) (~2*log2 n in
   practice), so operations are O(log n) on average.
 - Fix: self-balancing trees (AVL, Red-Black) or shuffle the input first.""")
