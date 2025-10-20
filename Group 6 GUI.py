import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random

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

class LinkedListStackGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.linked_list = SinglyLinkedList()

        self.title("New GUI")
        self.geometry("1600x700")

        self._setup_style()
        self.grid_columnconfigure(0, weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=3, minsize=600)
        self.grid_columnconfigure(2, weight=1, minsize=300)
        self.grid_rowconfigure(0, weight=1)

        linkedlist_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        linkedlist_panel.grid(row=0, column=0, sticky="nsew")

        center_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        center_panel.grid(row=0, column=1, sticky="nsew")

        stack_panel = ttk.Frame(self, padding="10", style="Dark.TFrame")
        stack_panel.grid(row=0, column=2, sticky="nsew")

        self._create_linkedlist_widgets(linkedlist_panel)
        self._create_center_widgets(center_panel)
        self._create_stack_widgets(stack_panel)

    def _create_linkedlist_widgets(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=0)
        parent.grid_columnconfigure(0, weight=1)

        ll_frame = ttk.LabelFrame(parent, text="LinkedList", padding="10", style="Dark.TLabelframe")
        ll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ll_frame.grid_columnconfigure(0, weight=1)
        ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(ll_frame, text="Node value:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.ll_entry = ttk.Entry(ll_frame)
        self.ll_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Button(ll_frame, text="Append", command=self.append_node, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), pady=4, sticky="ew", ipady=4)
        ttk.Button(ll_frame, text="Prepend", command=self.prepend_node, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), pady=4, sticky="ew", ipady=4)
        ttk.Button(ll_frame, text="Random nodes", command=self.add_random_nodes, style="Dark.TButton").grid(row=3, column=0, columnspan=2, padx=5, pady=4, sticky="ew", ipady=4)
        ttk.Button(ll_frame, text="Recursive traverse", command=self.recursive_traverse, style="Dark.TButton").grid(row=4, column=0, columnspan=2, padx=5, pady=4, sticky="ew", ipady=4)
        ttk.Button(ll_frame, text="Iterative traverse (use stack)", command=self.iterative_traverse_with_stack, style="Dark.TButton").grid(row=5, column=0, columnspan=2, padx=5, pady=4, sticky="ew", ipady=4)
        ttk.Button(ll_frame, text="Recursive reverse", command=self.recursive_reverse, style="Dark.TButton").grid(row=6, column=0, columnspan=2, padx=5, pady=4, sticky="ew", ipady=4)
        ttk.Button(ll_frame, text="Clear linked list", command=self.clear_linked_list, style="Dark.TButton").grid(row=7, column=0, columnspan=2, padx=5, pady=4, sticky="ew", ipady=4)
        
        ttk.Button(parent, text="Refresh Visualization", command=self.display_linked_list, style="Dark.TButton").grid(row=1, column=0, padx=10, pady=15, sticky="ew", ipady=12)

    def _create_center_widgets(self, parent):
        parent.grid_rowconfigure(0, weight=3)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        shapes_frame = ttk.LabelFrame(parent, text="Nodes", padding="10", style="Dark.TLabelframe")
        shapes_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        shapes_frame.grid_rowconfigure(0, weight=1)
        shapes_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(shapes_frame, bg="#2c2c2c", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        log_frame = ttk.LabelFrame(parent, text="LOG OUTPUT", padding="10", style="Dark.TLabelframe")
        log_frame.grid(row=1, column=0, sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, wrap="word", height=10, state="disabled", bg="#444444", fg="white", insertbackground="white", borderwidth=0)
        self.log_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def _create_stack_widgets(self, parent):
        parent.grid_rowconfigure(0, weight=0)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=0)
        parent.grid_columnconfigure(0, weight=1)

        stack_list_frame = ttk.LabelFrame(parent, text="Stack (from list)", padding="15", style="Dark.TLabelframe")
        stack_list_frame.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)
        stack_list_frame.grid_columnconfigure(0, weight=1)
        stack_list_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(stack_list_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        ttk.Entry(stack_list_frame).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        ttk.Button(stack_list_frame, text="Push", command=None, style="Big.Dark.TButton").grid(row=2, column=0, padx=(0, 2), pady=2, sticky="ew", ipady=5)
        ttk.Button(stack_list_frame, text="Pop", command=None, style="Big.Dark.TButton").grid(row=2, column=1, padx=(2, 0), pady=2, sticky="ew", ipady=5)
        ttk.Button(stack_list_frame, text="Clear", command=None, style="Big.Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew", ipady=5)

        stack_ll_frame = ttk.LabelFrame(parent, text="Stack (from LinkedList)", padding="15", style="Dark.TLabelframe")
        stack_ll_frame.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)
        stack_ll_frame.grid_columnconfigure(0, weight=1)
        stack_ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(stack_ll_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        ttk.Entry(stack_ll_frame).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        ttk.Button(stack_ll_frame, text="Push", command=None, style="Big.Dark.TButton").grid(row=2, column=0, padx=(0, 2), pady=2, sticky="ew", ipady=5)
        ttk.Button(stack_ll_frame, text="Pop", command=None, style="Big.Dark.TButton").grid(row=2, column=1, padx=(2, 0), pady=2, sticky="ew", ipady=5)
        ttk.Button(stack_ll_frame, text="Clear", command=None, style="Big.Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew", ipady=5)

        self.after(10, self.clear_log)


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
        style.configure("Dark.TLabelframe.Label", foreground=ACCENT_COLOR, background=FRAME_BG, font=("Segoe UI", 10, "bold"))
        style.configure("TEntry", fieldbackground=WIDGET_BG, foreground=FG_COLOR, insertcolor=ACCENT_COLOR, bordercolor=WIDGET_BG, relief="flat")
        style.configure("Dark.TButton", background=ACCENT_COLOR, foreground=BTN_FG, borderwidth=0, relief="flat", padding=5, font=("Segoe UI", 9, "bold"))
        style.map("Dark.TButton",
                  background=[('active', '#e67e22')],
                  foreground=[('active', BTN_FG)])

        style.configure("Big.Dark.TButton", background=ACCENT_COLOR, foreground=BTN_FG, borderwidth=0, relief="flat", padding=8, font=("Segoe UI", 10, "bold"))
        style.map("Big.Dark.TButton",
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
            nodes_data.insert(0, str(node.data))

        result = " -> ".join(nodes_data)
        self.log_message(f"Iterative traverse (stack): {result}")

    def recursive_reverse(self):
        if not self.linked_list.head:
            self.log_message("Cannot reverse an empty list.")
            return

        self.linked_list.head = self.linked_list.recursive_reverse_util(self.linked_list.head, None)
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
    temp_root = tk.Tk()
    temp_root.withdraw()

    splash_width = 400
    splash_height = 200
    screen_width = temp_root.winfo_screenwidth()
    screen_height = temp_root.winfo_screenheight()
    x = (screen_width // 2) - (splash_width // 2)
    y = (screen_height // 2) - (splash_height // 2)

    splash = tk.Toplevel(temp_root)
    splash.overrideredirect(True)
    splash.geometry(f'{splash_width}x{splash_height}+{x}+{y}')
    splash.config(bg="#121212")
    
    content_frame = tk.Frame(splash, bg="#121212")
    content_frame.pack(expand=True)

    try:
        gif_path = "loading.gif" 
        gif_image = Image.open(gif_path)
        
        gif_frames = []
        for i in range(gif_image.n_frames):
            gif_image.seek(i)
            frame = gif_image.resize((64, 64), Image.Resampling.LANCZOS)
            gif_frames.append(ImageTk.PhotoImage(frame))

        animation_label = tk.Label(content_frame, bg="#121212")
        animation_label.pack(pady=(0, 10))

        def update_animation(frame_index):
            frame = gif_frames[frame_index]
            animation_label.config(image=frame)
            next_frame_index = (frame_index + 1) % len(gif_frames)
            splash.after(10, update_animation, next_frame_index)

        update_animation(0)
    except FileNotFoundError:
        pass

    tk.Label(content_frame, text="Group 6", font=("Segoe UI", 18, "bold"), bg="#121212", fg="#ff9900").pack(pady=(0, 5))
    tk.Label(content_frame, text="Midterm Project", font=("Segoe UI", 12), bg="#121212", fg="#e0e0e0").pack(pady=(5, 0))

    def show_main_window():
        splash.destroy()
        temp_root.destroy()
        root.deiconify()

    root = LinkedListStackGUI()
    root.withdraw()
    root.after(3000, show_main_window)
    root.mainloop()