# stack_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# --- Custom Stack Exceptions ---
class StackOverflowError(Exception):
    """Exception raised for errors when stack is full."""
    pass

class StackUnderflowError(Exception):
    """Exception raised for errors when stack is empty."""
    pass

class Stack:
    """A simple LIFO stack implementation."""
    def __init__(self, capacity=10):
        self._items = []
        self.capacity = capacity
    
    def push(self, item):
        if len(self._items) >= self.capacity:
            raise StackOverflowError("Stack is full. Cannot push.")
        self._items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise StackUnderflowError("Stack is empty. Cannot pop.")
        return self._items.pop()
        
    def peek(self):
        if not self.is_empty():
            return self._items[-1]
        return None
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
        
    def to_list(self):
        return list(self._items)

    def search(self, item):
        """
        Searches for an item and returns its 1-based position from the top.
        The top of the stack is position 1.
        Returns None if the item is not found.
        """
        try:
            # self._items are stored with the bottom at index 0 and top at -1.
            # We reverse it to search from the top.
            return self._items[::-1].index(item) + 1
        except ValueError:
            return None

class StackPage(ttk.Frame):
    def __init__(self, parent_container, main_app):
        super().__init__(parent_container, style="Main.TFrame")
        self.main_app = main_app
        self.stack = Stack(capacity=10)
        
        # --- Create the Left/Right split ---
        self.horizontal_paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.horizontal_paned_window.pack(fill=tk.BOTH, expand=True)
        
        # --- Left Panel: Controls ---
        self.control_panel = ttk.Frame(self.horizontal_paned_window, width=250, style="Control.TFrame")
        self.horizontal_paned_window.add(self.control_panel, weight=1)

        # --- Right Panel: Representation ---
        self.representation_panel = ttk.Frame(self.horizontal_paned_window, relief="solid", borderwidth=1, style="Representation.TFrame")
        self.horizontal_paned_window.add(self.representation_panel, weight=3)
        
        self.create_control_widgets()
        self.create_representation_widgets()

        # --- Pre-load images ---
        self.overflow_img_tk = self._load_error_image("overflow.png")
        self.underflow_img_tk = self._load_error_image("underflow.png")

        # Apply theme immediately on creation
        self.apply_theme()

    def create_control_widgets(self):
        """Creates the controls for the left panel."""
        
        # --- Top Page Switcher Buttons ---
        top_btn_frame = ttk.Frame(self.control_panel)
        top_btn_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.list_btn = ttk.Button(top_btn_frame, text="List", command=lambda: self.main_app.switch_page("list"))
        self.list_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.recursion_btn = ttk.Button(top_btn_frame, text="Recursion Stack", command=lambda: self.main_app.switch_page("recursion"))
        self.recursion_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.stack_btn = ttk.Button(top_btn_frame, text="Stack", command=lambda: self.main_app.switch_page("stack"))
        self.stack_btn.pack(side=tk.LEFT, expand=True, padx=2)
        self.stack_btn.config(style="Accent.TButton")
        
        # --- Validation for numeric input ---
        vcmd = (self.register(self._validate_numeric_input), '%P')

        # --- Stack Specific Controls ---
        ttk.Label(self.control_panel, text="Entry Node Value:").pack(pady=(20, 0))
        self.node_value_var = tk.StringVar()
        self.node_value_entry = ttk.Entry(self.control_panel, 
                                          textvariable=self.node_value_var,
                                          validate='key', validatecommand=vcmd)
        self.node_value_entry.pack(fill=tk.X, padx=10, pady=5)
        
        action_btn_frame = ttk.Frame(self.control_panel)
        action_btn_frame.pack(pady=10)
        
        ttk.Button(action_btn_frame, text="Push", command=self.push_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Pop", command=self.pop_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Peek", command=self.peek_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Search", command=self.search_node).pack(side=tk.LEFT, padx=2)

        self.size_btn_var = tk.StringVar(value=f"No. of Elements in the Stack: {self.stack.size()}")
        ttk.Button(self.control_panel, textvariable=self.size_btn_var, command=self.show_size).pack(fill=tk.X, padx=10, pady=15)
        
        # Spacer
        ttk.Frame(self.control_panel, style="Main.TFrame").pack(fill='both', expand=True)

    def create_representation_widgets(self):
        """Creates the canvas for the right panel."""
        ttk.Label(self.representation_panel, text="Representation: LIFO Stack", style="Header.TLabel").pack(pady=5)

        self.canvas_frame = ttk.Frame(self.representation_panel, style="Canvas.TFrame")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas_v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.config(yscrollcommand=self.canvas_v_scroll.set)

    def apply_theme(self):
        """Applies the current theme from main_app to this page's widgets."""
        theme = self.main_app.theme
        
        # Define a new style for the active button
        self.main_app.style.configure("Accent.TButton", 
                                      background=theme["accent"], 
                                      foreground=theme["btn_fg"])
        self.main_app.style.map("Accent.TButton",
                                background=[('active', theme["accent_active"])])

        self.canvas.config(bg=theme["canvas_bg"])
        self.canvas_v_scroll.config(style="Vertical.TScrollbar")
        self.update_representation() # Redraw canvas

    def push_node(self):
        value = self.node_value_var.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value to push onto the stack.")
            return
        
        try:
            self.stack.push(int(value)) # Convert to int before pushing
            self.node_value_var.set("")
            self.main_app.log_output(f"Pushed {value} onto the stack.")
            self.update_representation()
        except StackOverflowError as e:
            self.main_app.log_output(f"Failed to Push: {e}")
            self.show_error_image_window("Stack Overflow", str(e), self.overflow_img_tk)

    def pop_node(self):
        try:
            popped_value = self.stack.pop()
            self.main_app.log_output(f"Popped {popped_value} from the stack.")
            self.update_representation()
        except StackUnderflowError as e:
            self.main_app.log_output(f"Failed to Pop: {e}")
            self.show_error_image_window("Stack Underflow", str(e), self.underflow_img_tk)

    def peek_node(self):
        try:
            peek_value = self.stack.peek()
            messagebox.showinfo("Peek Result", f"The top element is {peek_value}.")
            self.main_app.log_output(f"Peeked: Top element is {peek_value}.")
        except StackUnderflowError:
            self.main_app.log_output("Peeked: Stack is empty.")
            self.show_error_image_window("Stack Underflow", "The stack is empty. Nothing to peek at.", self.underflow_img_tk)

    def search_node(self):
        """Searches for a value in the stack and shows its position."""
        value = self.node_value_var.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value to search for.")
            return

        position = self.stack.search(int(value)) # Convert to int for searching

        if position is not None:
            messagebox.showinfo("Search Result", f"Element {value} found at position {position} from the top.")
            self.main_app.log_output(f"Search: Found {value} at position {position}.")
        else:
            messagebox.showinfo("Search Result", f"Element {value} not found in the stack.")
            self.main_app.log_output(f"Search: '{value}' not found.")

    def show_size(self):
        size = self.stack.size()
        self.size_btn_var.set(f"No. of Elements in the Stack: {size}")
        self.main_app.log_output(f"Stack size checked: {size} elements.")

    def update_representation(self):
        """Draws the stack blocks on the canvas (LIFO: blocks stacked vertically)."""
        self.canvas.delete("all")
        self.show_size() 
        theme = self.main_app.theme
        
        items = self.stack.to_list()
        capacity = self.stack.capacity
        frame_w, frame_h = 250, 40
        x_start, y_start = 50, 30
        y_spacing = 5
        
        self.canvas.create_text(x_start, 10, text=f"Capacity: {len(items)} / {capacity}", anchor="nw", fill=theme["fg"], font=("Arial", 10))

        if not items:
             self.canvas.create_text(x_start, y_start, text="The Stack is Empty.", 
                                      anchor="nw", fill=theme["fg"], font=("Arial", 12))
             bbox = self.canvas.bbox("all")
             self.canvas.config(scrollregion=bbox if bbox else (0, 0, 1, 1))
             return

        # Draw from bottom (index 0) to top (index -1)
        # We reverse the items so the "top" of the stack is at the top of the drawing
        for i, data in enumerate(reversed(items)):
            y_pos = y_start + i * (frame_h + y_spacing)
            x1, y1 = x_start, y_pos
            x2, y2 = x1 + frame_w, y1 + frame_h
            
            fill_color = theme["node_fill"]
            if i == 0: # This is the top-most item
                fill_color = theme["accent"] 
                self.canvas.create_text(x2 + 10, y1 + frame_h / 2, text="<-- TOP / PEEK", 
                                         anchor="w", fill=theme["head_color"], font=("Arial", 10, "bold"))

            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                         fill=fill_color, outline=theme["node_border"], width=1)
            
            self.canvas.create_text(x1 + frame_w / 2, y1 + frame_h / 2, text=str(data), 
                                     anchor="center", fill=theme["btn_fg"], font=("Arial", 10, "bold"))
            
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.config(scrollregion=(0, 0, bbox[2] + 150, bbox[3] + 50)) # Add padding
        else:
            self.canvas.config(scrollregion=(0, 0, 1, 1))

    def _validate_numeric_input(self, P):
        """Validates that the input is a digit or an empty string."""
        if P.isdigit() or P == "":
            return True
        self.bell() # Audible feedback for invalid input
        return False

    def _load_error_image(self, filename, size=(100, 100)):
        """Loads and resizes an image, returning an ImageTk.PhotoImage object."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, filename)
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(pil_image)
        except FileNotFoundError:
            self.main_app.log_output(f"Error: Image '{filename}' not found.")
            # Create a placeholder image if file not found
            placeholder = Image.new("RGB", size, "grey")
            return ImageTk.PhotoImage(placeholder)
        except Exception as e:
            self.main_app.log_output(f"Error loading image '{filename}': {e}")
            return None

    def show_error_image_window(self, title, message, image_tk):
        """Displays a Toplevel window with an image and a message."""
        if not image_tk:
            messagebox.showerror(title, message)
            return

        window = tk.Toplevel(self)
        window.title(title)
        window.transient(self.main_app) # Keep it on top of the main app
        window.grab_set() # Modal behavior
        window.resizable(False, False)

        theme = self.main_app.theme
        window.config(bg=theme["bg"])

        img_label = ttk.Label(window, image=image_tk, background=theme["bg"])
        img_label.pack(pady=(10, 5))

        msg_label = ttk.Label(window, text=message, wraplength=250, justify="center", background=theme["bg"], foreground=theme["fg"])
        msg_label.pack(pady=5, padx=10)

        ok_button = ttk.Button(window, text="OK", command=window.destroy, style="Accent.TButton")
        ok_button.pack(pady=(5, 10), ipadx=10)

        window.update_idletasks()
        x = self.main_app.winfo_x() + (self.main_app.winfo_width() // 2) - (window.winfo_width() // 2)
        y = self.main_app.winfo_y() + (self.main_app.winfo_height() // 2) - (window.winfo_height() // 2)

        window.geometry(f"+{x}+{y}")
