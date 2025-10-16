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

    def pop_head(self):
        """Removes and returns the head of the list."""
        if not self.head:
            return None
        popped_node = self.head
        self.head = self.head.next
        return popped_node.data
        
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

        # Main Layout
        self.grid_columnconfigure(0, weight=1, minsize=450)
        self.grid_columnconfigure(1, weight=2, minsize=800)
        self.grid_rowconfigure(0, weight=1)

        # --- Data Structure Instances ---
        self.linked_list = SinglyLinkedList()
        self.separate_stack = [] # For the "Stack (separate)" group

        self.title("Linked List & Stack Operations GUI")
        self.geometry("1400x650")

        # --- Create and Place Main Frames ---
        left_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        left_panel.grid(row=0, column=0, sticky="nsew")

        right_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew")

        self._create_left_panel_widgets(left_panel)
        self._create_right_panel_widgets(right_panel)
        
        # This ensures the window is drawn so we can get its size for wrapping
        self.update_idletasks()
        self.display_linked_list() # Initial draw

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
        self.canvas = tk.Canvas(parent, bg="#505050", highlightthickness=1, highlightbackground="#666666")
        self.canvas.grid(row=0, column=0, sticky="nsew")

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
        ttk.Button(ll_frame, text="Recursive traverse", command=self.recursive_traverse_action, style="Dark.TButton").grid(row=4, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Iterative traverse (use stack)", command=self.iterative_traverse_action, style="Dark.TButton").grid(row=5, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Recursive reverse", command=self.recursive_reverse_action, style="Dark.TButton").grid(row=6, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Clear linked list", command=self.clear_linked_list, style="Dark.TButton").grid(row=7, column=0, columnspan=2, pady=2, sticky="ew")

        # --- Stack (separate) Group ---
        stack_list_frame = ttk.LabelFrame(stack_controls_frame, text="Stack (separate)", padding="10", style="Dark.TLabelframe")
        stack_list_frame.grid(row=0, column=0, sticky="ew", pady=(5, 5))
        stack_list_frame.grid_columnconfigure(0, weight=1)
        stack_list_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(stack_list_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.stack_list_entry = ttk.Entry(stack_list_frame)
        self.stack_list_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(stack_list_frame, text="Push(list)", command=self.push_separate_stack, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(stack_list_frame, text="Pop(list)", command=self.pop_separate_stack, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(stack_list_frame, text="Clear stack(list)", command=self.clear_separate_stack, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

        # --- Stack on LinkedList Group ---
        stack_ll_frame = ttk.LabelFrame(stack_controls_frame, text="Stack built on LinkedList (push/pop head)", padding="10", style="Dark.TLabelframe")
        stack_ll_frame.grid(row=1, column=0, sticky="ew", pady=5)
        stack_ll_frame.grid_columnconfigure(0, weight=1)
        stack_ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(stack_ll_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.stack_ll_entry = ttk.Entry(stack_ll_frame)
        self.stack_ll_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(stack_ll_frame, text="Push(LL)", command=self.push_ll_stack, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(stack_ll_frame, text="Pop(LL)", command=self.pop_ll_stack, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(stack_ll_frame, text="Clear stack(LL)", command=self.clear_linked_list, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

        # --- Refresh Button ---
        ttk.Button(parent, text="Refresh visualization", command=self.display_linked_list, style="Dark.TButton").grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

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

    # --- Stack (Separate List) Methods ---
    def push_separate_stack(self):
        value = self.stack_list_entry.get()
        if not value: return
        self.separate_stack.append(value)
        self.log_message(f"Pushed '{value}' to separate stack. Stack: {self.separate_stack}")
        self.stack_list_entry.delete(0, tk.END)

    def pop_separate_stack(self):
        if not self.separate_stack:
            self.log_message("Separate stack is empty.")
            return
        value = self.separate_stack.pop()
        self.log_message(f"Popped '{value}' from separate stack. Stack: {self.separate_stack}")
        
    def clear_separate_stack(self):
        self.separate_stack.clear()
        self.log_message("Cleared separate stack.")
    
    # --- Stack (Linked List) Methods ---
    def push_ll_stack(self):
        value = self.stack_ll_entry.get()
        if not value: return
        self.linked_list.prepend(value) # Push is prepend for a LL stack
        self.log_message(f"Pushed '{value}' to LL stack.")
        self.stack_ll_entry.delete(0, tk.END)
        self.display_linked_list()

    def pop_ll_stack(self):
        value = self.linked_list.pop_head() # Pop is removing the head
        if value is None:
            self.log_message("LL stack is empty.")
        else:
            self.log_message(f"Popped '{value}' from LL stack.")
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
        
        self.draw_on_canvas(nodes)

    def draw_on_canvas(self, nodes):
        """Draws the nodes and arrows on the canvas, wrapping to a new line if needed."""
        self.canvas.delete("all")
        
        # Define drawing parameters
        start_x, y = 60, 100
        x = start_x
        y_spacing = 80
        node_w, node_h, arrow_len = 60, 40, 40
        canvas_width = self.canvas.winfo_width()
        padding = 50 # Keep nodes from touching the absolute edge

        # Draw the 'HEAD' label
        self.canvas.create_text(x - 35, y, text="HEAD", fill="white", font=("Segoe UI", 12))
        
        if not nodes:
            self.canvas.create_line(x, y, x + arrow_len, y, arrow='last', fill='white')
            self.canvas.create_text(x + arrow_len + 30, y, text="None", fill="white", font=("Segoe UI", 12))
            return

        for node_data in nodes:
            # --- WRAPPING LOGIC ---
            # Check if the NEXT node and arrow will go off-screen
            if x + arrow_len + node_w > canvas_width - padding:
                # Move to the next line
                y += y_spacing
                # Reset x to the start
                x = start_x
                # Optional: draw a "return" arrow
                self.canvas.create_line(x-arrow_len, y-y_spacing, x-arrow_len, y, arrow='last', fill='#cccccc', dash=(2, 4))

            # Draw the arrow pointing to the current node
            self.canvas.create_line(x, y, x + arrow_len, y, arrow='last', fill='white')
            x += arrow_len
            
            # Draw the node box and its text
            self.canvas.create_rectangle(x, y - node_h/2, x + node_w, y + node_h/2, fill="#ff9900", outline="white")
            self.canvas.create_text(x + node_w/2, y, text=node_data, fill="black", font=("Segoe UI", 10, "bold"))
            x += node_w

        # --- Final arrow to None (also checks for wrapping) ---
        if x + arrow_len > canvas_width - padding:
            y += y_spacing
            x = start_x
            self.canvas.create_line(x-arrow_len, y-y_spacing, x-arrow_len, y, arrow='last', fill='#cccccc', dash=(2, 4))
            
        self.canvas.create_line(x, y, x + arrow_len, y, arrow='last', fill='white')
        self.canvas.create_text(x + arrow_len + 30, y, text="None", fill="white", font=("Segoe UI", 12))

if __name__ == "__main__":
    app = LinkedListStackGUI()
    app.mainloop()