# linkedlist_page.py

import tkinter as tk
from tkinter import ttk, messagebox
import random

class LinkedListPage(ttk.Frame):
    def __init__(self, parent_container, main_app):
        super().__init__(parent_container, style="Main.TFrame")
        self.main_app = main_app
        self.active_list_type = "singly"
        
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
        self.list_btn.config(style="Accent.TButton") 
        
        self.recursion_btn = ttk.Button(top_btn_frame, text="Recursion Stack", command=lambda: self.main_app.switch_page("recursion"))
        self.recursion_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.stack_btn = ttk.Button(top_btn_frame, text="Stack", command=lambda: self.main_app.switch_page("stack"))
        self.stack_btn.pack(side=tk.LEFT, expand=True, padx=2)

        # --- Notebook (Singly, Doubly, Circular) ---
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

    def create_list_controls(self, parent_frame, list_type):
        """Creates the common control elements for each linked list type tab."""
        
        ttk.Label(parent_frame, text="Node Value:").pack(pady=(10, 0))
        entry_var = tk.StringVar()
        entry = ttk.Entry(parent_frame, textvariable=entry_var)
        entry.pack(fill=tk.X, padx=10, pady=5)
        setattr(self, f"{list_type}_entry_var", entry_var)

        action_btn_frame = ttk.Frame(parent_frame, style="NotebookTab.TFrame")
        action_btn_frame.pack(pady=5)
        
        ttk.Button(action_btn_frame, text="Append", command=lambda: self.perform_action(list_type, "append")).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Prepend", command=lambda: self.perform_action(list_type, "prepend")).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_btn_frame, text="Del", command=lambda: self.perform_action(list_type, "delete")).pack(side=tk.LEFT, padx=2)

        ttk.Button(parent_frame, text="Random Node", command=lambda: self.perform_action(list_type, "random")).pack(fill=tk.X, padx=10, pady=5) # Renamed button slightly
        ttk.Button(parent_frame, text="Reverse Order", command=lambda: self.perform_action(list_type, "reverse")).pack(fill=tk.X, padx=10, pady=5)
        
        # Spacer
        ttk.Frame(parent_frame, style="NotebookTab.TFrame").pack(fill='both', expand=True)

    def create_representation_widgets(self):
        """Creates the canvas for the right panel."""
        ttk.Label(self.representation_panel, text="Representation: Linked Lists", style="Header.TLabel").pack(pady=5)

        self.canvas_frame = ttk.Frame(self.representation_panel, style="Canvas.TFrame")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas_v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_h_scroll = ttk.Scrollbar(self.representation_panel, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas_h_scroll.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))
        
        self.canvas.config(yscrollcommand=self.canvas_v_scroll.set, xscrollcommand=self.canvas_h_scroll.set)

    def on_tab_change(self, event):
        """Updates active_list_type when a new tab is selected."""
        selected_tab = self.list_type_notebook.tab(self.list_type_notebook.select(), "text")
        if selected_tab == "Singly":
            self.active_list_type = "singly"
        elif selected_tab == "Doubly":
            self.active_list_type = "doubly"
        elif selected_tab == "Circular":
            self.active_list_type = "circular"
        self.main_app.log_output(f"Switched to {self.active_list_type.capitalize()} Linked List tab.")
        self.update_representation()

    def get_active_list_object(self):
        """Returns the currently active linked list object from main_app."""
        if self.active_list_type == "singly":
            return self.main_app.sll
        elif self.active_list_type == "doubly":
            return self.main_app.dll
        elif self.active_list_type == "circular":
            return self.main_app.cll
        return None

    def get_active_entry_var(self):
        """Returns the StringVar of the entry widget of the active tab."""
        entry_var_name = f"{self.active_list_type}_entry_var"
        return getattr(self, entry_var_name, None)

    def get_active_entry_value(self):
        """Returns the value from the entry widget of the active tab."""
        entry_var = self.get_active_entry_var()
        return entry_var.get() if entry_var else ""

    def perform_action(self, list_type, action):
        """Handles actions for linked lists."""
        linked_list = self.get_active_list_object()
        if not linked_list:
            return

        active_entry_var = self.get_active_entry_var()
        value = active_entry_var.get() if active_entry_var else ""
        
        if action == "append":
            if not value: return messagebox.showwarning("Input Error", "Please enter a value to append.")
            linked_list.add_node(value)
            self.main_app.log_output(f"Appended '{value}' to {list_type} list.")
            if active_entry_var: active_entry_var.set("") 

        elif action == "prepend":
            if not value: return messagebox.showwarning("Input Error", "Please enter a value to prepend.")
            linked_list.prepend_node(value)
            self.main_app.log_output(f"Prepended '{value}' to {list_type} list.")
            if active_entry_var: active_entry_var.set("") 

        elif action == "delete":
            if not value: return messagebox.showwarning("Input Error", "Please enter a value to delete.")
            if linked_list.delete_node(value):
                self.main_app.log_output(f"Deleted '{value}' from {list_type} list.")
                if active_entry_var: active_entry_var.set("") 
            else:
                messagebox.showerror("Deletion Error", f"Node '{value}' not found in {list_type} list.")
                self.main_app.log_output(f"Failed to delete '{value}' (not found) from {list_type} list.")
        
        elif action == "random":
            random_value = random.randint(1, 100) # Generate a random integer from 1 to 10
            linked_list.add_node(random_value)
            self.main_app.log_output(f"Added random node '{random_value}' to {list_type} list.")
        
        elif action == "reverse":
            linked_list.reverse()
            self.main_app.log_output(f"Reversed {list_type} list.")
        
        self.update_representation()

    def apply_theme(self):
        """Applies the current theme from main_app to this page's widgets."""
        theme = self.main_app.theme
        
        self.main_app.style.configure("Accent.TButton", 
                                      background=theme["accent"], 
                                      foreground=theme["btn_fg"])
        self.main_app.style.map("Accent.TButton",
                                background=[('active', theme["accent_active"])])
        
        self.canvas.config(bg=theme["canvas_bg"])
        self.canvas_v_scroll.config(style="Vertical.TScrollbar")
        self.canvas_h_scroll.config(style="Horizontal.TScrollbar")
        
        self.update_representation() 

    def update_representation(self):
        """Redraws the linked lists on the canvas."""
        self.canvas.delete("all")
        theme = self.main_app.theme

        node_width = 80
        node_height = 40
        x_offset = 50
        y_offset = 40
        y_spacing = 100
        
        self.draw_list_on_canvas(self.main_app.sll, "Singly", x_offset, y_offset, node_width, node_height)
        y_offset += y_spacing + node_height
        self.draw_list_on_canvas(self.main_app.dll, "Doubly", x_offset, y_offset, node_width, node_height)
        y_offset += y_spacing + node_height
        self.draw_list_on_canvas(self.main_app.cll, "Circular", x_offset, y_offset, node_width, node_height)

        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.config(scrollregion=(0, 0, bbox[2] + 50, bbox[3] + 50))
        else:
            self.canvas.config(scrollregion=(0, 0, 1, 1))

    def draw_list_on_canvas(self, linked_list_obj, list_name, start_x, start_y, node_w, node_h):
        """Draws a single linked list type on the canvas."""
        theme = self.main_app.theme
        
        self.canvas.create_text(start_x, start_y - 20, text=f"{list_name}:", anchor="nw",
                                 fill=theme["fg"], font=("Arial", 12, "bold"))
        
        nodes_data = linked_list_obj.to_list()
        
        if not nodes_data and list_name != "Circular":
            self.canvas.create_text(start_x + node_w + 10, start_y + node_h // 2, text="EMPTY", anchor="w",
                                     fill=theme["fg"], font=("Arial", 10))
            return
        
        current_x = start_x + 50
        
        self.canvas.create_text(current_x - 30, start_y + node_h // 2, text="Head", anchor="e",
                                 fill=theme["head_color"], font=("Arial", 10, "bold"))
        
        if list_name == "Circular" and not nodes_data:
            self.canvas.create_text(current_x + node_w // 2, start_y + node_h // 2, text="EMPTY", anchor="center",
                                     fill=theme["fg"], font=("Arial", 10))
            return

        for i, data in enumerate(nodes_data):
            x1, y1 = current_x, start_y
            x2, y2 = current_x + node_w, start_y + node_h
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=theme["node_fill"],
                                         outline=theme["node_border"], width=1)
            self.canvas.create_text(current_x + node_w / 2, start_y + node_h / 2, text=str(data),
                                     fill=theme["fg"], font=("Arial", 10))
            
            if i < len(nodes_data) - 1:
                arrow_start_x = x2
                arrow_end_x = current_x + node_w + 30
                self.canvas.create_line(arrow_start_x, start_y + node_h / 2,
                                         arrow_end_x, start_y + node_h / 2,
                                         arrow=tk.LAST, fill=theme["arrow_color"])
                
                if list_name == "Doubly":
                    self.canvas.create_line(arrow_end_x, start_y + node_h / 2 + 5,
                                             arrow_start_x, start_y + node_h / 2 + 5,
                                             arrow=tk.LAST, fill=theme["arrow_color"])
            
            current_x += node_w + 30

        if nodes_data:
            last_node_x1 = current_x - (node_w + 30)
            last_node_x2 = last_node_x1 + node_w
            
            if list_name in ["Singly", "Doubly"]:
                self.canvas.create_text(last_node_x2 + 30, start_y + node_h / 2, text="NULL", anchor="w",
                                         fill=theme["fg"], font=("Arial", 10))
            
            elif list_name == "Circular":
                head_node_x = start_x + 50
                last_node_end_x = last_node_x2
                arrow_y = start_y + node_h / 2

                p1_x, p1_y = last_node_end_x + 10, arrow_y
                p2_x, p2_y = p1_x + 20, start_y + node_h + 20 
                p3_x, p3_y = head_node_x - 20, p2_y
                p4_x, p4_y = head_node_x - 10, start_y + node_h / 2
                
                self.canvas.create_line(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y,

                                         smooth=True, arrow=tk.LAST, fill=theme["arrow_color"])
