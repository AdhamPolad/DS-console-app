"""DS Lab - entry point. Run:  python main.py"""
from array_structures import array_benchmark
from linked_lists import linked_list_benchmark, linked_list_demo
from stack_queue_deque import text_editor_undo_redo, print_queue_simulation, deque_menu
from hash_table import contact_book, hash_table_demo
from bst import bst_menu, bst_sorted_vs_random


def menu_linked_lists():
    while True:
        print("\n  1) Demo (operations on both lists)")
        print("  2) Performance comparison")
        print("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            linked_list_demo()
        elif c == "2":
            linked_list_benchmark()
        elif c == "0":
            return


def menu_stack_queue_deque():
    while True:
        print("\n  1) Text editor Undo/Redo      (Stack)")
        print("  2) Print queue                (Queue)")
        print("  3) Palindrome / History       (Deque)")
        print("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            text_editor_undo_redo()
        elif c == "2":
            print_queue_simulation()
        elif c == "3":
            deque_menu()
        elif c == "0":
            return


def menu_hash():
    while True:
        print("\n  1) Contact book (interactive)")
        print("  2) Performance / collision demo")
        print("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            contact_book()
        elif c == "2":
            hash_table_demo()
        elif c == "0":
            return


def menu_bst():
    while True:
        print("\n  1) Interactive BST (insert/search/delete)")
        print("  2) Sorted vs random insertion comparison")
        print("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            bst_menu()
        elif c == "2":
            bst_sorted_vs_random()
        elif c == "0":
            return


def main():
    while True:
        print("\n" + "=" * 50)
        print("         DS LAB - Data Structures")
        print("=" * 50)
        print(" 1. Array vs Dynamic Array (benchmark)")
        print(" 2. Singly vs Doubly Linked List")
        print(" 3. Stack, Queue, Deque (applications)")
        print(" 4. Hash Table (chaining) - Contact book")
        print(" 5. Binary Search Tree")
        print(" 0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            array_benchmark()
        elif choice == "2":
            menu_linked_lists()
        elif choice == "3":
            menu_stack_queue_deque()
        elif choice == "4":
            menu_hash()
        elif choice == "5":
            menu_bst()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
