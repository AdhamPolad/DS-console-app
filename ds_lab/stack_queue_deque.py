"""Topic 3: Stack, Queue and Deque with application features."""
from array_structures import DynamicArray
from linked_lists import SNode, DoublyLinkedList


class Stack:
    """LIFO - built on our DynamicArray (push/pop at the end are O(1))."""

    def __init__(self):
        self._arr = DynamicArray()

    def push(self, v): self._arr.append(v)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self._arr.delete_end()

    def peek(self):
        return self._arr._data[len(self._arr) - 1] if not self.is_empty() else None

    def is_empty(self): return len(self._arr) == 0
    def clear(self): self._arr = DynamicArray()
    def __len__(self): return len(self._arr)


class Queue:
    """FIFO - built on a singly linked list with head AND tail pointers,
    so enqueue and dequeue are both O(1)."""

    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def enqueue(self, v):
        node = SNode(v)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.size += 1

    def dequeue(self):
        if not self.head:
            raise IndexError("queue is empty")
        v = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return v

    def is_empty(self): return self.size == 0
    def __len__(self): return self.size

    def items(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out


class Deque:
    """Double-ended queue - built on the doubly linked list (all ends O(1))."""

    def __init__(self):
        self._dll = DoublyLinkedList()

    def add_front(self, v): self._dll.prepend(v)
    def add_back(self, v): self._dll.append(v)
    def remove_front(self): return self._dll.delete_first()
    def remove_back(self): return self._dll.delete_last()
    def is_empty(self): return len(self._dll) == 0
    def __len__(self): return len(self._dll)
    def items(self): return self._dll.to_list()


def text_editor_undo_redo():
    """STACK application: undo / redo."""
    print("\n--- Text Editor with Undo/Redo (two stacks) ---")
    print("Commands: write <text> | undo | redo | show | back")
    text = ""
    undo_stack, redo_stack = Stack(), Stack()
    while True:
        cmd = input("editor> ").strip()
        if cmd == "back":
            return
        if cmd.startswith("write "):
            undo_stack.push(text)
            redo_stack.clear()
            text += cmd[6:]
        elif cmd == "undo":
            if undo_stack.is_empty():
                print("Nothing to undo.")
            else:
                redo_stack.push(text)
                text = undo_stack.pop()
        elif cmd == "redo":
            if redo_stack.is_empty():
                print("Nothing to redo.")
            else:
                undo_stack.push(text)
                text = redo_stack.pop()
        elif cmd == "show":
            pass
        else:
            print("Unknown command.")
            continue
        print(f'Text: "{text}"   (undo steps: {len(undo_stack)}, redo steps: {len(redo_stack)})')


def print_queue_simulation():
    """QUEUE application: print jobs processed first-come-first-served."""
    print("\n--- Print Queue (FIFO) ---")
    print("Commands: add <document name> | print | show | back")
    q = Queue()
    while True:
        cmd = input("printer> ").strip()
        if cmd == "back":
            return
        if cmd.startswith("add "):
            q.enqueue(cmd[4:])
            print(f"Added. Jobs waiting: {len(q)}")
        elif cmd == "print":
            if q.is_empty():
                print("No jobs.")
            else:
                print(f"Printing: {q.dequeue()}")
        elif cmd == "show":
            print("Waiting:", q.items())
        else:
            print("Unknown command.")


def is_palindrome(text):
    """DEQUE application: compare from both ends."""
    dq = Deque()
    for ch in text.lower():
        if ch.isalnum():
            dq.add_back(ch)
    while len(dq) > 1:
        if dq.remove_front() != dq.remove_back():
            return False
    return True


def browser_history():
    """DEQUE application: keeps only the last 5 visited pages."""
    print("\n--- Recent History (Deque, max 5 items) ---")
    print("Type a page name to visit it. 'back' to leave, 'oldest' removes oldest.")
    history = Deque()
    while True:
        page = input("visit> ").strip()
        if page == "back":
            return
        if page == "oldest":
            print("Removed:", history.remove_front() if not history.is_empty() else "nothing")
        elif page:
            history.add_back(page)
            if len(history) > 5:
                print("Limit reached, removed oldest:", history.remove_front())
        print("History (oldest -> newest):", history.items())


def deque_menu():
    while True:
        print("\n  1) Palindrome checker (Deque)")
        print("  2) Recent history with size limit (Deque)")
        print("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            t = input("  Enter text: ")
            print("  Palindrome!" if is_palindrome(t) else "  Not a palindrome.")
        elif c == "2":
            browser_history()
        elif c == "0":
            return
