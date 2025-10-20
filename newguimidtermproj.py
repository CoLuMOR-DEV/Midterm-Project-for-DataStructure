import tkinter as tk
from tkinter import ttk, messagebox
import random
class Node:
    def __init__(self, data): # Node
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
        parent.grid_columnconfigure(0, weight=1)

        # Linked List Operations
        ll_frame = ttk.LabelFrame(parent, text="LinkedList", padding="10", style="Dark.TLabelframe")
        ll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ll_frame.grid_columnconfigure(0, weight=1)
        ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(ll_frame, text="Node value:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.ll_entry = ttk.Entry(ll_frame)
        self.ll_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(ll_frame, text="Append", command=None, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(ll_frame, text="Prepend", command=None, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(ll_frame, text="Random nodes", command=None, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Recursive traverse", command=None, style="Dark.TButton").grid(row=4, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Iterative traverse (use stack)", command=None, style="Dark.TButton").grid(row=5, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Recursive reverse", command=None, style="Dark.TButton").grid(row=6, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Clear linked list", command=None, style="Dark.TButton").grid(row=7, column=0, columnspan=2, pady=2, sticky="ew")
        ttk.Button(ll_frame, text="Refresh visualization", command=None, style="Dark.TButton").grid(row=8, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    def _create_center_widgets(self, parent):
        parent.grid_rowconfigure(0, weight=3)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Nodes Output
        shapes_frame = ttk.LabelFrame(parent, text="Nodes", padding="10", style="Dark.TLabelframe")
        shapes_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        shapes_frame.grid_rowconfigure(0, weight=1)
        shapes_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(shapes_frame, bg="#2c2c2c", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Log Output
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
        parent.grid_columnconfigure(0, weight=1)

        # Stack Operations
        stack_list_frame = ttk.LabelFrame(parent, text="Stack (from list)", padding="10", style="Dark.TLabelframe")
        stack_list_frame.grid(row=0, column=0, sticky="new", pady=5)
        stack_list_frame.grid_columnconfigure(0, weight=1)
        stack_list_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(stack_list_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        ttk.Entry(stack_list_frame).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        ttk.Button(stack_list_frame, text="Push", command=None, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(stack_list_frame, text="Pop", command=None, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(stack_list_frame, text="Clear", command=None, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

        stack_ll_frame = ttk.LabelFrame(parent, text="Stack (from LinkedList)", padding="10", style="Dark.TLabelframe")
        stack_ll_frame.grid(row=1, column=0, sticky="new", pady=5)
        stack_ll_frame.grid_columnconfigure(0, weight=1)
        stack_ll_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(stack_ll_frame, text="Value to push:", style="Dark.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        ttk.Entry(stack_ll_frame).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(stack_ll_frame, text="Push", command=None, style="Dark.TButton").grid(row=2, column=0, padx=(0, 2), sticky="ew")
        ttk.Button(stack_ll_frame, text="Pop", command=None, style="Dark.TButton").grid(row=2, column=1, padx=(2, 0), sticky="ew")
        ttk.Button(stack_ll_frame, text="Clear", command=None, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

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

if __name__ == "__main__":
    app = LinkedListStackGUI()
    app.mainloop()