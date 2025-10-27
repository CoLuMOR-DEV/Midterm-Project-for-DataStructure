# recursion_page.py

import tkinter as tk
from tkinter import ttk, messagebox

class RecursionPage(ttk.Frame):
    def __init__(self, parent_container, main_app):
        super().__init__(parent_container, style="Main.TFrame")
        self.main_app = main_app
        
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
        self.recursion_btn.config(style="Accent.TButton") # Active page
        
        self.stack_btn = ttk.Button(top_btn_frame, text="Stack", command=lambda: self.main_app.switch_page("stack"))
        self.stack_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        # --- Recursion Specific Controls ---
        ttk.Label(self.control_panel, text="Number of Elements (up-to 10):").pack(pady=(20, 0))
        self.num_elements_var = tk.StringVar(value="3")
        self.num_elements_entry = ttk.Entry(self.control_panel, textvariable=self.num_elements_var)
        self.num_elements_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(self.control_panel, text="Tail Recursion", 
                   command=lambda: self.run_recursion("tail")).pack(fill=tk.X, padx=10, pady=15)
        
        ttk.Button(self.control_panel, text="Head Recursion", 
                   command=lambda: self.run_recursion("head")).pack(fill=tk.X, padx=10, pady=5)

        # Spacer
        ttk.Frame(self.control_panel, style="Main.TFrame").pack(fill='both', expand=True)

    def create_representation_widgets(self):
        """Creates the canvas for the right panel."""
        ttk.Label(self.representation_panel, text="Representation: Recursion", style="Header.TLabel").pack(pady=5)

        self.canvas_frame = ttk.Frame(self.representation_panel, style="Canvas.TFrame")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas_v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.config(yscrollcommand=self.canvas_v_scroll.set)
        # No horizontal scroll needed for vertical stack

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

    def run_recursion(self, mode):
        """Simulates and visualizes a recursion function call stack."""
        try:
            num_elements = int(self.num_elements_var.get())
            if not 1 <= num_elements <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a number between 1 and 10 for the elements.")
            return

        self.main_app.log_output(f"Running {mode.capitalize()} Recursion simulation with {num_elements} elements.")
        
        stack_data = []
        if mode == "tail":
            # Simulate Tail Recursion (Output happens on the way down)
            for i in range(1, num_elements + 1):
                # --- CHANGED: Store only the number as the value ---
                stack_data.append((i, str(i), i)) # (call_num, value, order)
        elif mode == "head":
            # Simulate Head Recursion (Output happens on the way back up)
            temp_calls = []
            for i in range(1, num_elements + 1):
                # --- CHANGED: Store only the number as the value ---
                temp_calls.append((i, str(i))) # (call_num, value)
            
            # Reverse for the 'return' phase order
            for i, (call_num, value) in enumerate(reversed(temp_calls)):
                 # (call_num, value, order)
                 stack_data.append((call_num, value, i + 1))
        
        self.update_representation(mode, stack_data)

    def update_representation(self, mode=None, stack_data=None):
        """Draws the stack frames on the canvas."""
        self.canvas.delete("all")
        theme = self.main_app.theme
        
        if mode is None:
             self.canvas.create_text(10, 10, text="Run Tail or Head Recursion to view the stack.", 
                                      anchor="nw", fill=theme["fg"], font=("Arial", 12))
             return
             
        frame_w, frame_h = 200, 50
        x_start, y_start = 120, 30
        y_spacing = 20
        
        self.canvas.create_text(x_start, y_start - 20, 
                                 text=f"Function Call Stack ({mode.capitalize()})", 
                                 anchor="nw", fill=theme["fg"], font=("Arial", 12, "bold"))

        for i, (call_num, value, order) in enumerate(stack_data):
            x1, y1 = x_start, y_start + i * (frame_h + y_spacing)
            x2, y2 = x1 + frame_w, y1 + frame_h
            
            # 1. Draw the box
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                         fill=theme["node_fill"], outline=theme["node_border"], width=1)
            
            # 2. Draw ONLY the value INSIDE the box
            # --- CHANGED: Font size from 10 to 14 ---
            self.canvas.create_text(x1 + frame_w / 2, y1 + frame_h / 2, text=value, 
                                     anchor="center", fill=theme["fg"], font=("Arial", 14, "bold"))

            # 3. Draw the "Call" number OUTSIDE to the left
            self.canvas.create_text(x1 - 10, y1 + frame_h / 2, text=f"Call: {call_num}", 
                                     anchor="e", fill=theme["fg"], font=("Arial", 10))
            
            # 4. Draw the "Order" number OUTSIDE to the right
            self.canvas.create_text(x2 + 10, y1 + frame_h / 2, text=f"Order: {order}", 
                                     anchor="w", fill=theme["head_color"], font=("Arial", 10, "bold"))
            
            # Draw arrow connecting frames
            if i < len(stack_data) - 1:
                mid_x = x1 + frame_w / 2
                self.canvas.create_line(mid_x, y2, mid_x, y2 + y_spacing, arrow=tk.LAST, fill=theme["arrow_color"])

        bbox = self.canvas.bbox("all")
        if bbox:
            # Add padding to the scroll region to see the text on the right
            self.canvas.config(scrollregion=(0, 0, bbox[2] + 100, bbox[3] + 50))
        else:
            self.canvas.config(scrollregion=(0, 0, 1, 1))