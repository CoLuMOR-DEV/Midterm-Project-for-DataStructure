import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Data Structures ---
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

class LinkedListStackGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self._setup_style()

        # Main Layout
        self.grid_columnconfigure(0, weight=1, minsize=450)
        self.grid_columnconfigure(1, weight=2, minsize=800)
        self.grid_rowconfigure(0, weight=1)

        # --- Data Structure Instances ---
        self.linked_list = SinglyLinkedList()

        self.title("Linked List Operations GUI ONLYY")
        self.geometry("1400x650")


        # --- Create and Place Main Frames ---
        left_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        left_panel.grid(row=0, column=0, sticky="nsew")

        right_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew")

        self._create_left_panel_widgets(left_panel)
        self._create_right_panel_widgets(right_panel)

    def _create_left_panel_widgets(self, parent):
        parent.grid_rowconfigure(0, weight=3)
        parent.grid_rowconfigure(1, weight=2)
        parent.grid_columnconfigure(0, weight=1)

        controls_frame = ttk.Frame(parent, style="Dark.TFrame")
        controls_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self._create_control_buttons(controls_frame)

        log_frame = ttk.LabelFrame(parent, text="Output / Log", padding="10", style="Dark.TLabelframe")
        log_frame.grid(row=1, column=0, sticky="nsew")
        self._create_log_area(log_frame)

    def _create_right_panel_widgets(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self._create_visualization(parent)

    def _create_visualization(self, parent):
        canvas = tk.Canvas(parent, bg="#505050", highlightthickness=1, highlightbackground="#666666")
        canvas.grid(row=0, column=0, sticky="nsew")

    def _create_log_area(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(parent, wrap="word", height=10, state="disabled", bg="#444444", fg="white", insertbackground="white")
        self.log_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.clear_log()

    def _create_control_buttons(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        stack_controls_frame = ttk.Frame(parent, style="Dark.TFrame")
        stack_controls_frame.grid(row=0, column=1, sticky="ns", padx=(5, 0))

        # Linked List Operation Buttons
        ll_frame = ttk.LabelFrame(parent, text="LinkedList operations", padding="10", style="Dark.TLabelframe")
        ll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, rowspan=2)
        ll_frame.grid_columnconfigure(0, weight=1)
        ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(ll_frame, text="Node value:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.ll_entry = ttk.Entry(ll_frame)
        self.ll_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        ttk.Button(ll_frame, text="Append", command=self.append_node, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(ll_frame, text="Prepend", command=self.prepend_node, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(ll_frame, text="Random nodes", command=self.add_random_nodes, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Recursive traverse", command=self.recursive_traverse, style="Dark.TButton").grid(row=4, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Iterative traverse (use stack)", command=self.iterative_traverse_with_stack, style="Dark.TButton").grid(row=5, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Recursive reverse", command=self.recursive_reverse, style="Dark.TButton").grid(row=6, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Clear linked list", command=self.clear_linked_list, style="Dark.TButton").grid(row=7, column=0, columnspan=2, pady=2, sticky="ew")

        # --- Stack (separate) Group ---
        stack_list_frame = ttk.LabelFrame(stack_controls_frame, text="Stack (separate)", padding="10", style="Dark.TLabelframe")
        stack_list_frame.grid(row=0, column=0, sticky="ew", pady=(5, 5))
        stack_list_frame.grid_columnconfigure(0, weight=1)
        stack_list_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(stack_list_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        ttk.Entry(stack_list_frame).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(stack_list_frame, text="Push(list)", command=None, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(stack_list_frame, text="Pop(list)", command=None, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(stack_list_frame, text="Clear stack(list)", command=None, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

        # --- Stack on LinkedList Group ---
        stack_ll_frame = ttk.LabelFrame(stack_controls_frame, text="Stack built on LinkedList (push/pop head)", padding="10", style="Dark.TLabelframe")
        stack_ll_frame.grid(row=1, column=0, sticky="ew", pady=5)
        stack_ll_frame.grid_columnconfigure(0, weight=1)
        stack_ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(stack_ll_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        ttk.Entry(stack_ll_frame).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(stack_ll_frame, text="Push(LL)", command=None, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(stack_ll_frame, text="Pop(LL)", command=None, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(stack_ll_frame, text="Clear stack(LL)", command=None, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

        # --- Refresh Button ---
        ttk.Button(parent, text="Refresh visualization", command=self.display_linked_list, style="Dark.TButton").grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    def _setup_style(self):
        BG_COLOR = "#121212"
        FG_COLOR = "#e0e0e0"
        FRAME_BG = "#1e1e1e"
        WIDGET_BG = "#2c2c2c"
        ACCENT_COLOR = "#ff9900"
        BTN_FG = "black"
        
        self.configure(bg=BG_COLOR)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Dark.TFrame", background=FRAME_BG)
        style.configure("Dark.TLabel", foreground=FG_COLOR, background=FRAME_BG)
        style.configure("Dark.TLabelframe", background=FRAME_BG, bordercolor=WIDGET_BG, relief="solid", borderwidth=1)
        style.configure("Dark.TLabelframe.Label", foreground=ACCENT_COLOR, background=FRAME_BG, font=("Segoe UI", 9, "bold"))
        
        style.configure("TEntry", fieldbackground=WIDGET_BG, foreground=FG_COLOR, insertcolor=ACCENT_COLOR, bordercolor=WIDGET_BG, relief="flat")
        
        style.configure("Dark.TButton", background=ACCENT_COLOR, foreground=BTN_FG, borderwidth=0, relief="flat", font=("Segoe UI", 9, "bold"))
        style.map("Dark.TButton",
                  background=[('active', '#e67e22')],
                  foreground=[('active', BTN_FG)])

    # --- Log/Output Methods ---
    def log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")

    # --- LinkedList Operation Methods ---
    def append_node(self):
        value = self.ll_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value for the node.")
            return
        self.linked_list.append(value)
        self.log_message(f"Appended node with value: {value}")
        self.ll_entry.delete(0, tk.END)
        self.display_linked_list()

    def prepend_node(self):
        value = self.ll_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value for the node.")
            return
        self.linked_list.prepend(value)
        self.log_message(f"Prepended node with value: {value}")
        self.ll_entry.delete(0, tk.END)
        self.display_linked_list()

    def add_random_nodes(self):
        for _ in range(5):
            value = random.randint(1, 100)
            self.linked_list.append(value)
            self.log_message(f"Appended random node: {value}")
        self.display_linked_list()

    def clear_linked_list(self):
        self.linked_list.head = None
        self.log_message("Linked list cleared.")
        self.display_linked_list()

    def recursive_traverse(self):
        if not self.linked_list.head:
            self.log_message("Recursive traverse: List is empty.")
            return

        nodes_data = []
        def _traverse(node):
            if node:
                nodes_data.append(str(node.data))
                _traverse(node.next)

        _traverse(self.linked_list.head)
        result = " -> ".join(nodes_data)
        self.log_message(f"Recursive traverse: {result}")

    def iterative_traverse_with_stack(self):
        if not self.linked_list.head:
            self.log_message("Iterative traverse (stack): List is empty.")
            return

        stack = []
        current = self.linked_list.head
        while current:
            stack.append(current)
            current = current.next

        nodes_data = []
        while stack:
            node = stack.pop()
            nodes_data.insert(0, str(node.data)) # Insert at beginning to maintain order

        result = " -> ".join(nodes_data)
        self.log_message(f"Iterative traverse (stack): {result}")

    def recursive_reverse(self):
        if not self.linked_list.head:
            self.log_message("Cannot reverse an empty list.")
            return

        def _reverse(current, prev):
            if not current:
                return prev
            next_node = current.next
            current.next = prev
            return _reverse(next_node, current)

        self.linked_list.head = _reverse(self.linked_list.head, None)
        self.log_message("Linked list reversed recursively.")
        self.display_linked_list()

    def display_linked_list(self):
        """Displays the current state of the linked list in the log."""
        nodes = []
        current = self.linked_list.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        
        if not nodes:
            display_str = "List is empty."
        else:
            display_str = " -> ".join(nodes) + " -> None"

        self.log_message("-" * 30)
        self.log_message(f"Current List: {display_str}")
        self.log_message("-" * 30)

if __name__ == "__main__":
    app = LinkedListStackGUI()

    app.mainloop()