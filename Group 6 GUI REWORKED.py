import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import random

# --- Singly Linked List ---
class SLL_Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = SLL_Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def prepend_node(self, data):
        new_node = SLL_Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_node(self, key):
        temp = self.head
        if temp and temp.data == key:
            self.head = temp.next
            return True
        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next
        if not temp:
            return False
        prev.next = temp.next
        return True

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr.data)
            curr = curr.next
        return nodes

# --- Doubly Linked List ---
class DLL_Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = DLL_Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def prepend_node(self, data):
        new_node = DLL_Node(data)
        if self.head:
            self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def delete_node(self, key):
        curr = self.head
        while curr and curr.data != key:
            curr = curr.next
        if not curr:
            return False

        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next
            
        if curr.next:
            curr.next.prev = curr.prev
        return True

    def reverse(self):
        temp = None
        current = self.head
        while current:
            temp = current.prev
            current.prev = current.next
            current.next = temp
            current = current.prev
        
        if temp:
            self.head = temp.prev

    def to_list(self):
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr.data)
            curr = curr.next
        return nodes

# --- Circular Linked List ---
class CLL_Node: 
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = CLL_Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def prepend_node(self, data):
        new_node = CLL_Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head
            self.head = new_node

    def delete_node(self, key):
        if not self.head:
            return False

        curr = self.head
        prev = None

        while True:
            if curr.data == key:
                break
            prev = curr
            curr = curr.next
            if curr == self.head:
                return False

        if curr == self.head:
            if curr.next == self.head:
                self.head = None
            else:
                last = self.head
                while last.next != self.head:
                    last = last.next
                last.next = self.head.next
                self.head = self.head.next
        else:
            prev.next = curr.next
        return True

    def reverse(self):
        if not self.head or self.head.next == self.head:
            return

        temp_list = []
        current = self.head
        while True:
            temp_list.append(current.data)
            current = current.next
            if current == self.head:
                break
        
        temp_list.reverse()
        
        self.head = None
        for data in temp_list:
            self.add_node(data)

    def to_list(self):
        nodes = []
        if not self.head:
            return nodes
        curr = self.head
        while True:
            nodes.append(curr.data)
            curr = curr.next
            if curr == self.head:
                break
        return nodes

# --- GUI CLASSES ----------------------------------------------

class SplashScreen(tk.Toplevel):
    """Splash screen with animated GIF and custom text"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Loading...")
        self.parent = parent
        self.frames = []
        self.frame_index = 0
        
        self.config(bg="#F0F0F0")

        try:
            gif_size = (100, 100)
            self.gif_image = Image.open("loading.gif")
            while True:
                resized_frame = self.gif_image.copy().resize(gif_size, Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(resized_frame))
                self.gif_image.seek(len(self.frames))
        except EOFError:
            pass
        except FileNotFoundError:
            self.frames.append(ImageTk.PhotoImage(Image.new("RGB", (200, 100), "#F0F0F0")))
            self.label = tk.Label(self, text="loading.gif not found!", bg="#F0F0F0", font=("Arial", 10))
        
        if self.frames and not hasattr(self, 'label'):
            self.label = tk.Label(self, image=self.frames[0], bg="#F0F0F0", bd=0)
        
        self.label.pack(padx=10, pady=(10, 5)) 

        self.group_label = tk.Label(
            self, 
            text="Group 6", 
            font=("Arial", 16, "bold"), 
            bg="#F0F0F0"
        )
        self.group_label.pack(pady=(0, 5))

        self.project_label = tk.Label(
            self, 
            text="Midterm Project", 
            font=("Arial", 12), 
            bg="#F0F0F0"
        )
        self.project_label.pack(pady=(0, 10))

        self.geometry("300x180")

        self.center_window()
        
        self.overrideredirect(True)
        
        self.frame_count = len(self.frames)
        if self.frame_count > 1:
            self.animate()

    def center_window(self):
        """Centers the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def animate(self):
        """Cycles through the GIF frames"""
        self.frame_index = (self.frame_index + 1) % self.frame_count
        self.label.config(image=self.frames[self.frame_index])
        try:
            delay = self.gif_image.info.get('duration', 100)
        except AttributeError:
            delay = 100
        self.after(delay, self.animate)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Linked List Visualizer")
        self.geometry("1000x650")

        self.withdraw()

        self.sll = SinglyLinkedList()
        self.dll = DoublyLinkedList()
        self.cll = CircularLinkedList()
        self.active_list_type = "singly"

        self.current_theme = "light"
        self.light_theme = {
            "bg": "white", "fg": "black", "btn_bg": "lightgray", "btn_fg": "black",
            "accent": "#007acc", "accent_active": "#005f9e",
            "canvas_bg": "white", "node_fill": "#ADD8E6", "node_border": "black",
            "arrow_color": "black", "head_color": "darkgreen", "log_bg": "#F0F0F0", "log_fg": "black"
        }
        self.dark_theme = {
            "bg": "#2E2E2E", "fg": "white", "btn_bg": "#4A4A4A", "btn_fg": "white",
            "accent": "#ff9900", "accent_active": "#e67e22",
            "canvas_bg": "#3A3A3A", "node_fill": "#6A5ACD", "node_border": "white",
            "arrow_color": "white", "head_color": "lightgreen", "log_bg": "#1C1C1C", "log_fg": "white"
        }
        self.theme = self.light_theme

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.create_widgets()
        self.apply_theme(self.current_theme)
        self.update_representation()
        self.log_output("Application started.")

    def create_widgets(self):
        self.vertical_paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.vertical_paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.top_frame = ttk.Frame(self.vertical_paned_window, style="Main.TFrame")
        self.vertical_paned_window.add(self.top_frame, weight=3)

        self.bottom_frame = ttk.Frame(self.vertical_paned_window, style="Main.TFrame")
        self.vertical_paned_window.add(self.bottom_frame, weight=1)

        # --- Top Frame Layout ---
        self.horizontal_paned_window = ttk.PanedWindow(self.top_frame, orient=tk.HORIZONTAL)
        self.horizontal_paned_window.pack(fill=tk.BOTH, expand=True)
        
        self.control_panel = ttk.Frame(self.horizontal_paned_window, width=250, style="Control.TFrame")
        self.horizontal_paned_window.add(self.control_panel, weight=1)

        # Right Representation Panel
        self.representation_panel = ttk.Frame(self.horizontal_paned_window, relief="solid", borderwidth=1)
        self.horizontal_paned_window.add(self.representation_panel, weight=3)

        # --- Control Panel Contents ---
        top_btn_frame = ttk.Frame(self.control_panel)
        top_btn_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.list_btn = ttk.Button(top_btn_frame, text="List", command=lambda: self.set_view_mode("list"))
        self.list_btn.pack(side=tk.LEFT, expand=True, padx=2)
        self.recursion_btn = ttk.Button(top_btn_frame, text="Recursion", command=lambda: self.log_output("Recursion view not yet implemented."))
        self.recursion_btn.pack(side=tk.LEFT, expand=True, padx=2)
        self.stack_btn = ttk.Button(top_btn_frame, text="Stack", command=lambda: self.log_output("Stack view not yet implemented."))
        self.stack_btn.pack(side=tk.LEFT, expand=True, padx=2)

        self.list_type_notebook = ttk.Notebook(self.control_panel)
        self.list_type_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.list_type_notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        self.sll_frame = ttk.Frame(self.list_type_notebook, style="NotebookTab.TFrame")
        self.dll_frame = ttk.Frame(self.list_type_notebook, style="NotebookTab.TFrame")
        self.cll_frame = ttk.Frame(self.list_type_notebook, style="NotebookTab.TFrame")

        self.list_type_notebook.add(self.sll_frame, text="Singly")
        self.list_type_notebook.add(self.dll_frame, text="Doubly")
        self.list_type_notebook.add(self.cll_frame, text="Circular")
        
        self.create_list_controls(self.sll_frame, "singly")
        self.create_list_controls(self.dll_frame, "doubly")
        self.create_list_controls(self.cll_frame, "circular")

        # --- Representation Panel Contents ---
        ttk.Label(self.representation_panel, text="Representation", style="Header.TLabel").pack(pady=5)

        self.canvas_frame = ttk.Frame(self.representation_panel, style="Canvas.TFrame")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas_v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_h_scroll = ttk.Scrollbar(self.representation_panel, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas_h_scroll.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))
        
        self.canvas.config(yscrollcommand=self.canvas_v_scroll.set, xscrollcommand=self.canvas_h_scroll.set)

        # --- Bottom Frame Layout ---
        self.log_frame = ttk.LabelFrame(self.bottom_frame, text="Log-Output", padding=10)
        self.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        
        self.log_text = tk.Text(self.log_frame, height=8, state=tk.DISABLED, font=("Courier", 10), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_scroll = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.log_scroll.set)

        self.themes_frame = ttk.LabelFrame(self.bottom_frame, text="Themes", padding=10)
        self.themes_frame.pack(side=tk.RIGHT, padx=(5, 10), pady=10)
        
        self.light_mode_btn = ttk.Button(self.themes_frame, text="Light Mode", command=lambda: self.apply_theme("light"))
        self.light_mode_btn.pack(pady=5)
        self.dark_mode_btn = ttk.Button(self.themes_frame, text="Dark Mode", command=lambda: self.apply_theme("dark"))
        self.dark_mode_btn.pack(pady=5)

    def create_list_controls(self, parent_frame, list_type):
        """Creates the common control elements for each linked list type tab."""
        
        ttk.Label(parent_frame, text="Node Value:").pack(pady=(10, 0))
        entry_var = tk.StringVar()
        entry = ttk.Entry(parent_frame, textvariable=entry_var)
        entry.pack(fill=tk.X, padx=10, pady=5)
        setattr(self, f"{list_type}_entry_var", entry_var)

        action_btn_frame = ttk.Frame(parent_frame)
        action_btn_frame.pack(pady=5)
        
        ttk.Button(action_btn_frame, text="Append", command=lambda: self.perform_action(list_type, "append")).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Prepend", command=lambda: self.perform_action(list_type, "prepend")).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Del", command=lambda: self.perform_action(list_type, "delete")).pack(side=tk.LEFT, padx=2)

        ttk.Button(parent_frame, text="Random Nodes", command=lambda: self.perform_action(list_type, "random")).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(parent_frame, text="Reverse Order", command=lambda: self.perform_action(list_type, "reverse")).pack(fill=tk.X, padx=10, pady=5)

    def on_tab_change(self, event):
        """Updates active_list_type when a new tab is selected."""
        selected_tab = self.list_type_notebook.tab(self.list_type_notebook.select(), "text")
        if selected_tab == "Singly":
            self.active_list_type = "singly"
        elif selected_tab == "Doubly":
            self.active_list_type = "doubly"
        elif selected_tab == "Circular":
            self.active_list_type = "circular"
        self.log_output(f"Switched to {self.active_list_type.capitalize()} Linked List tab.")
        self.update_representation()

    def get_active_list_object(self):
        """Returns the currently active linked list object."""
        if self.active_list_type == "singly":
            return self.sll
        elif self.active_list_type == "doubly":
            return self.dll
        elif self.active_list_type == "circular":
            return self.cll
        return None

    def get_active_entry_value(self):
        """Returns the value from the entry widget of the active tab."""
        entry_var_name = f"{self.active_list_type}_entry_var"
        entry_var = getattr(self, entry_var_name, None)
        return entry_var.get() if entry_var else ""

    def log_output(self, message):
        """Adds a message to the log output area."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def perform_action(self, list_type, action):
        """Handles actions for linked lists based on active type and action."""
        linked_list = self.get_active_list_object()
        if not linked_list:
            return

        value = self.get_active_entry_value()
        
        if action == "append":
            if not value:
                messagebox.showwarning("Input Error", "Please enter a value to append.")
                return
            linked_list.add_node(value)
            self.log_output(f"Appended '{value}' to {list_type} list.")
        elif action == "prepend":
            if not value:
                messagebox.showwarning("Input Error", "Please enter a value to prepend.")
                return
            linked_list.prepend_node(value)
            self.log_output(f"Prepended '{value}' to {list_type} list.")
        elif action == "delete":
            if not value:
                messagebox.showwarning("Input Error", "Please enter a value to delete.")
                return
            if linked_list.delete_node(value):
                self.log_output(f"Deleted '{value}' from {list_type} list.")
            else:
                messagebox.showerror("Deletion Error", f"Node '{value}' not found in {list_type} list.")
                self.log_output(f"Failed to delete '{value}' (not found) from {list_type} list.")
        elif action == "random":
            num_nodes_str = messagebox.askstring("Random Nodes", "How many random nodes to add? (1-10)")
            try:
                num_nodes = int(num_nodes_str)
                if not 1 <= num_nodes <= 10:
                    raise ValueError
            except (ValueError, TypeError):
                messagebox.showerror("Input Error", "Please enter a number between 1 and 10.")
                return
            
            for _ in range(num_nodes):
                random_value = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", str(random.randint(10,99))])
                linked_list.add_node(random_value)
                self.log_output(f"Added random node '{random_value}' to {list_type} list.")
        elif action == "reverse":
            linked_list.reverse()
            self.log_output(f"Reversed {list_type} list.")
        
        self.update_representation()

    def set_view_mode(self, mode):
        if mode == "list":
            self.log_output("Switched to List (Linked List) view.")
        else:
            self.log_output(f"SwM-o-d-e-d to {mode.capitalize()} view (not fully implemented).")

    def apply_theme(self, theme_name):
        """Applies the selected theme to all widgets."""
        if theme_name == "light":
            self.theme = self.light_theme
        elif theme_name == "dark":
            self.theme = self.dark_theme
        self.current_theme = theme_name

        self.config(bg=self.theme["bg"])

        self._configure_ttk_styles()
        
        self.canvas.config(bg=self.theme["canvas_bg"])
        self.log_text.config(bg=self.theme["log_bg"], fg=self.theme["log_fg"],
                             insertbackground=self.theme["fg"])

        self.update_representation()
        self.log_output(f"Switched to {theme_name.capitalize()} Mode.")

    def _configure_ttk_styles(self):
        """Configures all ttk styles based on the current theme."""
        self.style.configure("TFrame", background=self.theme["bg"])
        self.style.configure("Main.TFrame", background=self.theme["bg"])
        
        self.style.configure("Control.TFrame", background=self.theme["bg"], relief="solid", borderwidth=1, bordercolor=self.theme["fg"])
        self.style.configure("Representation.TFrame", background=self.theme["bg"], relief="solid", borderwidth=1, bordercolor=self.theme["fg"])
        self.style.configure("Canvas.TFrame", background=self.theme["bg"], relief="sunken", borderwidth=2, bordercolor=self.theme["fg"])
        self.style.configure("NotebookTab.TFrame", background=self.theme["bg"])

        self.style.configure("TPanedwindow", background=self.theme["bg"])

        self.style.configure("TLabel", background=self.theme["bg"], foreground=self.theme["fg"])
        self.style.configure("Header.TLabel", background=self.theme["bg"], foreground=self.theme["fg"], font=("Arial", 14, "bold"))

        self.style.configure("TLabelframe", background=self.theme["bg"], bordercolor=self.theme["fg"], relief="solid", borderwidth=1)
        self.style.configure("TLabelframe.Label", foreground=self.theme["fg"], background=self.theme["bg"])
        self.style.configure("Log.TLabelframe", background=self.theme["bg"], bordercolor=self.theme["fg"], relief="solid", borderwidth=1)
        self.style.configure("Log.TLabelframe.Label", foreground=self.theme["fg"], background=self.theme["bg"])

        self.style.configure("TButton", background=self.theme["btn_bg"], foreground=self.theme["btn_fg"],
                             borderwidth=0, relief="flat", padding=5)
        self.style.map("TButton",
                       background=[('active', self.theme["accent_active"])],
                       foreground=[('active', self.theme["btn_fg"])])

        self.style.configure("TEntry", fieldbackground=self.theme["log_bg"], foreground=self.theme["log_fg"],
                             insertcolor=self.theme["fg"], borderwidth=1, relief="solid")

        self.style.configure("TNotebook", background=self.theme["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.theme["btn_bg"], foreground=self.theme["btn_fg"], padding=[10, 5])
        self.style.map("TNotebook.Tab",
                       background=[("selected", self.theme["accent"]), ("active", self.theme["accent_active"])],
                       foreground=[("selected", self.theme["btn_fg"]), ("active", self.theme["btn_fg"])])

        self.style.configure("Vertical.TScrollbar", background=self.theme["btn_bg"], troughcolor=self.theme["bg"])
        self.style.map("Vertical.TScrollbar", background=[('active', self.theme["accent_active"])])
        self.style.configure("Horizontal.TScrollbar", background=self.theme["btn_bg"], troughcolor=self.theme["bg"])
        self.style.map("Horizontal.TScrollbar", background=[('active', self.theme["accent_active"])])

        # Apply scrollbar styles to specific scrollbars
        self.canvas_v_scroll.config(style="Vertical.TScrollbar")
        self.canvas_h_scroll.config(style="Horizontal.TScrollbar")
        self.log_scroll.config(style="Vertical.TScrollbar")

    def update_representation(self):
        self.canvas.delete("all")

        node_width = 80
        node_height = 40
        x_offset = 50
        y_offset = 40
        y_spacing = 100
        
        # Draw Singly Linked List
        self.draw_list_on_canvas(self.sll, "Singly", x_offset, y_offset, node_width, node_height)

        # Draw Doubly Linked List
        y_offset += y_spacing + node_height # Move down for next list
        self.draw_list_on_canvas(self.dll, "Doubly", x_offset, y_offset, node_width, node_height)

        # Draw Circular Linked List
        y_offset += y_spacing + node_height # Move down for next list
        self.draw_list_on_canvas(self.cll, "Circular", x_offset, y_offset, node_width, node_height)

        bbox = self.canvas.bbox("all")
        self.canvas.config(scrollregion=bbox if bbox else (0, 0, 1, 1))

    def draw_list_on_canvas(self, linked_list_obj, list_name, start_x, start_y, node_w, node_h):
        """Draws a single linked list type on the canvas."""
        
        self.canvas.create_text(start_x, start_y - 20, text=f"{list_name}:", anchor="nw",
                                fill=self.theme["fg"], font=("Arial", 12, "bold"))
        
        nodes_data = linked_list_obj.to_list()
        
        if not nodes_data and list_name != "Circular":
            self.canvas.create_text(start_x + node_w + 10, start_y + node_h // 2, text="EMPTY", anchor="w",
                                    fill=self.theme["fg"], font=("Arial", 10))
            return
        
        current_x = start_x + 50
        
        self.canvas.create_text(current_x - 30, start_y + node_h // 2, text="Head", anchor="e",
                                fill=self.theme["head_color"], font=("Arial", 10, "bold"))
        
        if list_name == "Circular" and not nodes_data:
            self.canvas.create_text(current_x + node_w // 2, start_y + node_h // 2, text="EMPTY", anchor="center",
                                    fill=self.theme["fg"], font=("Arial", 10))
            return


        for i, data in enumerate(nodes_data):
            x1, y1 = current_x, start_y
            x2, y2 = current_x + node_w, start_y + node_h
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.theme["node_fill"],
                                         outline=self.theme["node_border"], width=1)
            self.canvas.create_text(current_x + node_w / 2, start_y + node_h / 2, text=str(data),
                                    fill=self.theme["fg"], font=("Arial", 10))
            
            if i < len(nodes_data) - 1:
                arrow_start_x = x2
                arrow_end_x = current_x + node_w + 30
                self.canvas.create_line(arrow_start_x, start_y + node_h / 2,
                                        arrow_end_x, start_y + node_h / 2,
                                        arrow=tk.LAST, fill=self.theme["arrow_color"])
                
                if list_name == "Doubly":
                    self.canvas.create_line(arrow_end_x, start_y + node_h / 2,
                                            arrow_start_x, start_y + node_h / 2,
                                            arrow=tk.LAST, fill=self.theme["arrow_color"])
            
            current_x += node_w + 30

        if nodes_data:
            last_node_x1 = current_x - (node_w + 30)
            last_node_x2 = last_node_x1 + node_w
            
            if list_name == "Singly":
                self.canvas.create_text(last_node_x2 + 30, start_y + node_h / 2, text="NULL", anchor="w",
                                        fill=self.theme["fg"], font=("Arial", 10))
            elif list_name == "Doubly":
                self.canvas.create_text(last_node_x2 + 30, start_y + node_h / 2, text="NULL", anchor="w",
                                        fill=self.theme["fg"], font=("Arial", 10))
            elif list_name == "Circular":
                head_node_x = start_x + 50
                
                # Text "Back to Head"
                self.canvas.create_text(current_x + 50, start_y + node_h / 2, text="Back to Head", anchor="w",
                                        fill=self.theme["fg"], font=("Arial", 10))
                
                
                last_node_end_x = last_node_x2
                arrow_y = start_y + node_h / 2

                p1_x, p1_y = last_node_end_x + 10, arrow_y
                
                p2_x, p2_y = p1_x + 20, start_y + node_h + 20
                
                p3_x, p3_y = head_node_x - 20, p2_y
                
                p4_x, p4_y = head_node_x - 10, start_y + node_h / 2
                
                self.canvas.create_line(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y,
                                        smooth=True, arrow=tk.LAST, fill=self.theme["arrow_color"])
                
                self.canvas.create_text(start_x + 50 - 30, start_y + node_h / 2, text="Head", anchor="e",
                                fill=self.theme["head_color"], font=("Arial", 10, "bold"))


# --- Main execution ---
def main():
    app = MainApp()
    splash = SplashScreen(app)
    
    def show_main_app():
        splash.destroy()
        app.deiconify()
        app.lift()

    app.after(3000, show_main_app)
    app.mainloop()

if __name__ == "__main__":
    main()