# recursion_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import os

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
        
        # --- Image related attributes ---
        self.burger_image_tk = None
        self.current_burger_ids = [] 
        self.animation_delay_ms = 700 
        self.spongebob_frames = []
        self.spongebob_gif_image = None
        self.spongebob_animation_job = None
        self.patrick_frames = []
        self.patrick_gif_image = None
        self.patrick_animation_job = None

        self._load_burger_image()
        self._load_spongebob_gif()
        self._load_patrick_gif()

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
        self.recursion_btn.config(style="Accent.TButton")

        self.stack_btn = ttk.Button(top_btn_frame, text="Stack", command=lambda: self.main_app.switch_page("stack"))
        self.stack_btn.pack(side=tk.LEFT, expand=True, padx=2)

        # --- Recursion Specific Controls ---
        ttk.Label(self.control_panel, text="Number of Elements (up-to 10):").pack(pady=(20, 0))
        self.num_elements_var = tk.StringVar(value="3")
        self.num_elements_entry = ttk.Entry(self.control_panel, textvariable=self.num_elements_var)
        self.num_elements_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self.control_panel, text="Head Recursion",
                   command=lambda: self.run_recursion("head")).pack(fill=tk.X, padx=10, pady=15)

        ttk.Button(self.control_panel, text="Tail Recursion",
                   command=lambda: self.run_recursion("tail")).pack(fill=tk.X, padx=10, pady=5)

        # Spacer
        ttk.Frame(self.control_panel, style="Main.TFrame").pack(fill='both', expand=True)

    def create_representation_widgets(self):
        """Creates the canvas for the right panel."""
        ttk.Label(self.representation_panel, text="Representation: Recursion Sequence", style="Header.TLabel").pack(pady=5) # Renamed slightly

        self.canvas_frame = ttk.Frame(self.representation_panel, style="Canvas.TFrame")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) # Changed pack side

        # --- ADDED Horizontal Scrollbar ---
        self.canvas_h_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure canvas to use the scrollbar
        self.canvas.config(xscrollcommand=self.canvas_h_scroll.set)

    def _load_burger_image(self):
        """Loads and resizes the burger image."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        burger_path = os.path.join(script_dir, "burger.jpg")
        
        try:
            # Define a target size for the burger image
            target_size = (100, 50) # Matches frame_w, frame_h
            
            original_image = Image.open(burger_path)
            resized_image = original_image.resize(target_size, Image.Resampling.LANCZOS)
            self.burger_image_tk = ImageTk.PhotoImage(resized_image)
            self.main_app.log_output(f"Loaded burger.jpg from {burger_path}")
        except FileNotFoundError:
            self.main_app.log_output(f"Error: burger.jpg not found at {burger_path}. Using placeholder.")
            # Create a placeholder image if not found
            self.burger_image_tk = ImageTk.PhotoImage(Image.new("RGB", (100, 50), "#FFD700")) # Gold color placeholder
            self.canvas.create_text(50, 50, text="burger.jpg missing!", fill="red", font=("Arial", 12, "bold"))
        except Exception as e:
            self.main_app.log_output(f"Error loading burger.jpg: {e}. Using placeholder.")
            # Handle other potential PIL errors
            self.burger_image_tk = ImageTk.PhotoImage(Image.new("RGB", (100, 50), "#FFD700"))
            self.canvas.create_text(50, 50, text=f"Image Error: {e}", fill="red", font=("Arial", 10))

    def _load_spongebob_gif(self):
        """Loads and resizes the spongebob.gif frames."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, "spongebob.gif")

        try:
            self.spongebob_gif_image = Image.open(gif_path)
            gif_size = (200, 150) 
            
            for frame in ImageSequence.Iterator(self.spongebob_gif_image):
                resized_frame = frame.copy().resize(gif_size, Image.Resampling.LANCZOS)
                self.spongebob_frames.append(ImageTk.PhotoImage(resized_frame))
            
            if not self.spongebob_frames:
                 raise Exception("No frames found in GIF.")
            
            self.main_app.log_output(f"Loaded spongebob.gif from {gif_path}")

        except FileNotFoundError:
            self.main_app.log_output(f"Warning: spongebob.gif not found at {gif_path}. Animation will be skipped.")
            self.spongebob_frames = []
        except Exception as e:
            self.main_app.log_output(f"Error loading spongebob.gif: {e}. Animation will be skipped.")
            self.spongebob_frames = []

    def _load_patrick_gif(self):
        """Loads and resizes the patrick.gif frames."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, "patrick.gif")

        try:
            self.patrick_gif_image = Image.open(gif_path)
            gif_size = (150, 150) # A good size for below the burgers
            
            for frame in ImageSequence.Iterator(self.patrick_gif_image):
                resized_frame = frame.copy().resize(gif_size, Image.Resampling.LANCZOS)
                self.patrick_frames.append(ImageTk.PhotoImage(resized_frame))
            
            if not self.patrick_frames:
                 raise Exception("No frames found in GIF.")
            
            self.main_app.log_output(f"Loaded patrick.gif from {gif_path}")

        except FileNotFoundError:
            self.main_app.log_output(f"Warning: patrick.gif not found at {gif_path}. Animation will be skipped.")
            self.patrick_frames = []
        except Exception as e:
            self.main_app.log_output(f"Error loading patrick.gif: {e}. Animation will be skipped.")
            self.patrick_frames = []

    def apply_theme(self):
        """Applies the current theme from main_app to this page's widgets."""
        theme = self.main_app.theme

        self.main_app.style.configure("Accent.TButton",
                                      background=theme["accent"],
                                      foreground=theme["btn_fg"])
        self.main_app.style.map("Accent.TButton",
                                background=[('active', theme["accent_active"])])

        self.canvas.config(bg=theme["canvas_bg"])
        # --- Apply style to horizontal scrollbar ---
        self.canvas_h_scroll.config(style="Horizontal.TScrollbar")
        self.update_representation() 

    def run_recursion(self, mode):
        """Simulates and visualizes a recursion function sequence."""
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
            for i in range(1, num_elements + 1):
                stack_data.append((i, str(i), i))
        elif mode == "head":
            temp_calls = []
            for i in range(1, num_elements + 1):
                temp_calls.append((i, str(i)))

            for i, (call_num, value) in enumerate(reversed(temp_calls)):
                 stack_data.append((call_num, value, i + 1)) # (call_num, value, order)

        # Clear any pending animations
        if hasattr(self, '_animation_job_id'):
            self.after_cancel(self._animation_job_id)

        # Also cancel any spongebob animation
        if self.spongebob_animation_job:
            self.after_cancel(self.spongebob_animation_job)

        if self.patrick_animation_job:
            self.after_cancel(self.patrick_animation_job)

        if mode == "head":
            self.canvas.delete("all") # Clear canvas first
            self.animate_spongebob(callback=lambda: self.start_head_animation(mode, stack_data))
        else:
            self.update_representation(mode, stack_data)
            self.animate_patrick()
            self._animation_job_id = self.after(1000, lambda: self.animate_pop_out(mode))

    def update_representation(self, mode=None, stack_data=None, draw_burgers=True):
        """Draws the sequence frames horizontally on the canvas."""
        self.canvas.delete("all")
        theme = self.main_app.theme

        if mode is None or not stack_data:
             self.canvas.create_text(10, 10, text="Run Tail or Head Recursion to view the sequence.",
                                      anchor="nw", fill=theme["fg"], font=("Arial", 12))
             self.canvas.config(scrollregion=(0,0,1,1)) # Reset scrollregion
             return

        # --- Adjustments for Horizontal Layout ---
        frame_w, frame_h = 100, 50 
        x_start, y_start = 50, 50 
        x_spacing = 40 
        
        self.current_burger_ids = [] 

        title_text = ""
        if mode == "head":
            title_text = "Cooked Burgers Serving . . ."
        elif mode == "tail":
            title_text = "Patrick is Eating the Burgers . . ."

        self.canvas.create_text(x_start, y_start - 30,
                                 text=title_text, anchor="nw",
                                 fill=theme["fg"], font=("Arial", 12, "bold"))

        for i, (call_num, value, order) in enumerate(stack_data):
            center_x = x_start + i * (frame_w + x_spacing) + frame_w / 2
            center_y = y_start + frame_h / 2

            if draw_burgers:
                if self.burger_image_tk:
                    burger_id = self.canvas.create_image(center_x, center_y, image=self.burger_image_tk, tags="burger_image")
                    self.current_burger_ids.append(burger_id)
                else:
                    x1, y1 = center_x - frame_w / 2, center_y - frame_h / 2
                    x2, y2 = center_x + frame_w / 2, center_y + frame_h / 2
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=theme["node_fill"], outline=theme["node_border"], width=1)
                    self.canvas.create_text(center_x, center_y, text=value, anchor="center", fill=theme["fg"], font=("Arial", 14, "bold"))

        # Update scrollregion for horizontal scrolling
        bbox = self.canvas.bbox("all")
        if bbox:
            # bbox is (x_min, y_min, x_max, y_max)
            # Add padding for text below/right
            self.canvas.config(scrollregion=(0, 0, bbox[2] + 50, bbox[3] + 30))
        else:
            self.canvas.config(scrollregion=(0, 0, 1, 1))

    def start_head_animation(self, mode, stack_data):
        """Helper to begin the head recursion animation after the GIF."""
        self.update_representation(mode, stack_data, draw_burgers=False)
        self._animation_job_id = self.after(100, lambda: self.animate_appear(stack_data))

    def animate_spongebob(self, callback):
        """Plays the spongebob GIF animation and then calls the callback."""
        if not self.spongebob_frames:
            # If GIF failed to load, just run the callback immediately.
            callback()
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        center_x, center_y = canvas_w / 2, canvas_h / 2

        gif_item = self.canvas.create_image(center_x, center_y, image=self.spongebob_frames[0])
        
        # Run the GIF for one full cycle
        duration_per_frame = self.spongebob_gif_image.info.get('duration', 100)
        total_duration = duration_per_frame * len(self.spongebob_frames)

        def _animate_frame(frame_index):
            self.canvas.itemconfig(gif_item, image=self.spongebob_frames[frame_index])
            next_frame_index = (frame_index + 1) % len(self.spongebob_frames)
            self.spongebob_animation_job = self.after(duration_per_frame, lambda: _animate_frame(next_frame_index))

        _animate_frame(0)

        # Schedule the end of the animation
        self.after(total_duration + 100, lambda: [
            self.after_cancel(self.spongebob_animation_job), self.canvas.delete(gif_item), callback()
        ])

    def animate_patrick(self):
        """Plays the patrick GIF on a loop."""
        if not self.patrick_frames:
            return

        # Position below the burgers
        x_start, y_start = 50, 50
        frame_h = 50
        center_x = self.canvas.winfo_width() / 2
        center_y = y_start + frame_h + 100 

        gif_item = self.canvas.create_image(center_x, center_y, image=self.patrick_frames[0], tags="patrick_gif")
        
        duration_per_frame = self.patrick_gif_image.info.get('duration', 100)

        def _animate_frame(frame_index):
            if self.canvas.find_withtag(gif_item):
                self.canvas.itemconfig(gif_item, image=self.patrick_frames[frame_index])
                next_frame_index = (frame_index + 1) % len(self.patrick_frames)
                self.patrick_animation_job = self.after(duration_per_frame, lambda: _animate_frame(next_frame_index))
        _animate_frame(0)

    def animate_appear(self, stack_data):
        """Animates the 'appearing' of burgers from left to right for head recursion."""
        self.current_burger_ids = [] # Ensure it's clean before starting

        frame_w, frame_h = 100, 50
        x_start, y_start = 50, 50
        x_spacing = 40

        def _step(index):
            if index < len(stack_data):
                center_x = x_start + index * (frame_w + x_spacing) + frame_w / 2
                center_y = y_start + frame_h / 2

                if self.burger_image_tk:
                    burger_id = self.canvas.create_image(center_x, center_y, image=self.burger_image_tk, tags="burger_image")
                    self.current_burger_ids.append(burger_id)
                
                self._animation_job_id = self.after(self.animation_delay_ms, lambda: _step(index + 1))

        _step(0)

    def animate_pop_out(self, mode):
        """Animates the 'popping out' of burgers from the recursion sequence."""
        if not self.current_burger_ids:
            return
        
        if mode == "tail":
            removal_indices = list(range(len(self.current_burger_ids)))
        
        def _step(index):
            if index < len(removal_indices):
                burger_id = self.current_burger_ids[removal_indices[index]]
                self.canvas.delete(burger_id)
                self._animation_job_id = self.after(self.animation_delay_ms, lambda: _step(index + 1))
            else:
                if self.patrick_animation_job:
                    self.after_cancel(self.patrick_animation_job)
                    self.canvas.delete("patrick_gif")
                    self.patrick_animation_job = None

        _step(0)

