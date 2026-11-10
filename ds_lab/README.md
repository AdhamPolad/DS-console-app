# DS Lab - Data Structures Console Application

A console application written in Python (standard library only) that demonstrates
five basic data structures, with performance measurements and small practical features.

## How to run

```
python main.py
```

Requires Python 3.8 or newer. No external packages are needed.

## Project structure

```
ds_lab/
├── main.py                # menu and entry point
├── utils.py               # timing helper and table printing
├── array_structures.py    # Topic 1: static array, dynamic array, benchmark
├── linked_lists.py        # Topic 2: singly / doubly linked list, benchmark
├── stack_queue_deque.py   # Topic 3: Stack, Queue, Deque + applications
├── hash_table.py          # Topic 4: hash table with chaining + contact book
├── bst.py                 # Topic 5: binary search tree
└── README.md
```

## Topics and why each structure was used

### 1. Array and Dynamic Array
- `StaticArray` has a fixed capacity. `DynamicArray` doubles its capacity when full
  and halves it when only a quarter is used. Python's built-in `list` is added as a reference.
- The benchmark measures insert at end / beginning, delete from beginning / end and
  search for n = 1000, 5000, 10000.
- **Result:** operations at the beginning are O(n) because elements must shift.
  Appending is O(1) (amortized for the dynamic array). Search is O(n).
  The built-in list is much faster because it is implemented in C.

### 2. Singly and Doubly Linked Lists
- Both lists are implemented from scratch (prepend, append, delete first/last/value, search).
- The singly list only keeps a head pointer. The doubly list keeps head, tail and `prev` links.
- **Result:** inserting at the head is O(1) for both. Appending and deleting the last
  element are O(n) in the singly list but O(1) in the doubly list. The doubly list uses
  more memory but can be traversed backwards.

### 3. Stack, Queue and Deque
| Structure | Feature in the app | Why |
|-----------|--------------------|-----|
| Stack (LIFO), built on `DynamicArray` | Text editor with Undo / Redo | The last change must be undone first |
| Queue (FIFO), built on a linked list with head and tail | Print queue | Documents are printed in the order they arrive |
| Deque, built on the doubly linked list | Palindrome checker, recent history limited to 5 items | Needs fast access to both ends |

### 4. Hash Table (chaining)
- Own implementation: polynomial string hash, each bucket is a list of key/value pairs.
- Resizes (rehashes) when the load factor is above 0.75.
- Used as a contact book (name -> phone). The app also prints collision statistics and
  compares lookup time with a linear search in a list.

### 5. Binary Search Tree
- Insert, search (counts comparisons), delete (leaf, one child, two children), in-order traversal, height.
- **Sorted vs random insertion:** inserting sorted data always goes to one side, so the tree
  degenerates into a linked list (height = n, operations O(n)). Random data gives a
  height of about log n and O(log n) average operations. Self-balancing trees (AVL, Red-Black)
  solve this problem.



