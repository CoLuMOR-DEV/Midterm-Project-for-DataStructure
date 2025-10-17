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
        """Adds a node to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def _reverse_recursive_helper(self, current, prev):
        """Helper function for recursive reverse."""
        if not current:
            return prev
        next_node = current.next
        current.next = prev
        return self._reverse_recursive_helper(next_node, current)

    def reverse_recursive(self):
        """Kicks off the recursive reverse."""
        if self.head:
            self.head = self._reverse_recursive_helper(self.head, None)

class LinkedListStackGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self._setup_style()

        # Instances
        self.linked_list = SinglyLinkedList()

        self.title("Group 6 Midterm Project")
        self.geometry("1400x650")

        left_panel = ttk.Frame(self, padding="5", style="Dark.TFrame")
        left_panel.place(relx=0, rely=0, relwidth=0.33, relheight=1.0)

        right_panel = ttk.Frame(self, padding="5", style="Dark.TFrame")
        right_panel.place(relx=0.33, rely=0, relwidth=0.67, relheight=1)

        self._create_left_panel_widgets(left_panel)
        self._create_right_panel_widgets(right_panel)
        self.update_idletasks()
        self.display_linked_list()

    def _create_left_panel_widgets(self, parent):
        controls_frame = ttk.Frame(parent, style="Dark.TFrame")
        controls_frame.place(relx=0, rely=0, relwidth=1, relheight=0.65)
        self._create_control_buttons(controls_frame)

        log_frame = ttk.LabelFrame(parent, text="Output / Log", padding="10", style="Dark.TLabelframe")
        log_frame.place(relx=0, rely=0.65, relwidth=1, relheight=0.35, y=5)
        self._create_log_area(log_frame)

    def _create_right_panel_widgets(self, parent):
        self._create_visualization(parent)

    def _create_visualization(self, parent):
        self.canvas = tk.Canvas(parent, bg="#505050", highlightthickness=1, highlightbackground="#666666")
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _create_log_area(self, parent):
        self.log_text = tk.Text(parent, wrap="word", height=10, state="disabled", bg="#444444", fg="white", insertbackground="white")
        self.log_text.place(relx=0, rely=0, relwidth=1, relheight=1)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.log_text.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.log_text.config(yscrollcommand=scrollbar.set)
        self.clear_log()

    def _create_control_buttons(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        stack_controls_frame = ttk.Frame(parent, style="Dark.TFrame")
        stack_controls_frame.grid(row=0, column=1, sticky="nsew", padx=(5,0))

        # Linked List Operation Buttons
        ll_frame = ttk.LabelFrame(parent, text="LinkedList operations", padding="10", style="Dark.TLabelframe")
        ll_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5))

        ttk.Label(ll_frame, text="Node value:", style="Dark.TLabel").pack(fill='x', pady=(0, 5))
        self.ll_entry = ttk.Entry(ll_frame)
        self.ll_entry.pack(fill='x', pady=(0, 5))
        
        btn_frame1 = ttk.Frame(ll_frame, style="Dark.TFrame")
        btn_frame1.pack(fill='x')
        ttk.Button(btn_frame1, text="Append", command=self.append_node, style="Dark.TButton").pack(side='left', fill='x', expand=True, padx=(0, 2))
        ttk.Button(btn_frame1, text="Prepend", command=self.prepend_node, style="Dark.TButton").pack(side='left', fill='x', expand=True, padx=(2, 0))
        
        ttk.Button(ll_frame, text="Random nodes", command=self.add_random_nodes, style="Dark.TButton").pack(fill='x', pady=2)
        ttk.Button(ll_frame, text="Recursive traverse", command=self.recursive_traverse_action, style="Dark.TButton").pack(fill='x', pady=2)
        ttk.Button(ll_frame, text="Iterative traverse (use stack)", command=self.iterative_traverse_action, style="Dark.TButton").pack(fill='x', pady=2)
        ttk.Button(ll_frame, text="Recursive reverse", command=self.recursive_reverse_action, style="Dark.TButton").pack(fill='x', pady=2)
        ttk.Button(ll_frame, text="Clear linked list", command=self.clear_linked_list, style="Dark.TButton").pack(fill='x', pady=2)

        # --- Stack (separate) Group ---
        stack_list_frame = ttk.LabelFrame(stack_controls_frame, text="Stack (separate)", padding="10", style="Dark.TLabelframe")
        stack_list_frame.pack(fill='x', pady=(5, 5))
        
        ttk.Label(stack_list_frame, text="Value to push:", style="Dark.TLabel").pack(fill='x', pady=(0, 5))
        self.stack_list_entry = ttk.Entry(stack_list_frame)
        self.stack_list_entry.pack(fill='x', pady=(0, 5))

        btn_frame2 = ttk.Frame(stack_list_frame, style="Dark.TFrame")
        btn_frame2.pack(fill='x')
        ttk.Button(btn_frame2, text="Push(list)", command=None, style="Dark.TButton").pack(side='left', fill='x', expand=True, padx=(0, 2))
        ttk.Button(btn_frame2, text="Pop(list)", command=None, style="Dark.TButton").pack(side='left', fill='x', expand=True, padx=(2, 0))
        ttk.Button(stack_list_frame, text="Clear stack(list)", command=None, style="Dark.TButton").pack(fill='x', pady=2)

        # --- Stack on LinkedList Group ---
        stack_ll_frame = ttk.LabelFrame(stack_controls_frame, text="Stack built on LinkedList (push/pop head)", padding="10", style="Dark.TLabelframe")
        stack_ll_frame.pack(fill='x', pady=5)

        ttk.Label(stack_ll_frame, text="Value to push:", style="Dark.TLabel").pack(fill='x', pady=(0, 5))
        self.stack_ll_entry = ttk.Entry(stack_ll_frame)
        self.stack_ll_entry.pack(fill='x', pady=(0, 5))

        btn_frame3 = ttk.Frame(stack_ll_frame, style="Dark.TFrame")
        btn_frame3.pack(fill='x')
        ttk.Button(btn_frame3, text="Push(LL)", command=None, style="Dark.TButton").pack(side='left', fill='x', expand=True, padx=(0, 2))
        ttk.Button(btn_frame3, text="Pop(LL)", command=None, style="Dark.TButton").pack(side='left', fill='x', expand=True, padx=(2, 0))
        ttk.Button(stack_ll_frame, text="Clear stack(LL)", command=None, style="Dark.TButton").pack(fill='x', pady=2)

        ttk.Button(parent, text="Refresh visualization", command=self.display_linked_list, style="Dark.TButton").grid(row=1, column=0, columnspan=2, pady=(10,0), sticky="ew")

    def _setup_style(self):
        BG_COLOR, FG_COLOR, FRAME_BG = "#121212", "#e0e0e0", "#1e1e1e"
        WIDGET_BG, ACCENT_COLOR, BTN_FG = "#2c2c2c", "#ff9900", "black"
        self.configure(bg=BG_COLOR)
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("Dark.TFrame", background=FRAME_BG)
        style.configure("Dark.TLabel", foreground=FG_COLOR, background=FRAME_BG)
        style.configure("Dark.TLabelframe", background=FRAME_BG, bordercolor=WIDGET_BG, relief="solid")
        style.configure("Dark.TLabelframe.Label", foreground=ACCENT_COLOR, background=FRAME_BG, font=("Segoe UI", 9, "bold"))
        style.configure("TEntry", fieldbackground=WIDGET_BG, foreground=FG_COLOR, insertcolor=ACCENT_COLOR)
        style.configure("Dark.TButton", background=ACCENT_COLOR, foreground=BTN_FG, borderwidth=0, font=("Segoe UI", 9, "bold"))
        style.map("Dark.TButton", background=[('active', '#e67e22')], foreground=[('active', BTN_FG)])

    def log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")

    def append_node(self):
        value = self.ll_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value for the node.")
            return
        self.linked_list.append(value)
        self.log_message(f"Appended node: {value}")
        self.ll_entry.delete(0, tk.END)
        self.display_linked_list()

    def prepend_node(self):
        value = self.ll_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value for the node.")
            return
        self.linked_list.prepend(value)
        self.log_message(f"Prepended node: {value}")
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

    def recursive_traverse_action(self):
        nodes = []
        def _traverse(node):
            if node:
                nodes.append(str(node.data))
                _traverse(node.next)
        _traverse(self.linked_list.head)
        result = " -> ".join(nodes) if nodes else "Empty"
        self.log_message(f"Recursive traverse: {result}")

    def iterative_traverse_action(self):
        if not self.linked_list.head:
            self.log_message("Iterative traverse: List is empty")
            return
        
        nodes, stack = [], [self.linked_list.head]
        while stack:
            current = stack.pop()
            nodes.append(str(current.data))
            if current.next:
                stack.append(current.next)
        result = " -> ".join(nodes)
        self.log_message(f"Iterative traverse (using a stack): {result}")

    def recursive_reverse_action(self):
        self.linked_list.reverse_recursive()
        self.log_message("Reversed the linked list recursively.")
        self.display_linked_list()

    def display_linked_list(self):
        nodes = []
        current = self.linked_list.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        
        display_str = " -> ".join(nodes) + " -> None" if nodes else "List is empty."
        self.log_message("-" * 40)
        self.log_message(f"Current List: {display_str}")
        self.log_message("-" * 40)
        
        self.draw_on_canvas()

    def draw_on_canvas(self):
        """Clears the canvas."""
        self.canvas.delete("all")

if __name__ == "__main__":
    app = LinkedListStackGUI()
    app.mainloop()
