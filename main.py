import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import random
import os
import pygame

from linkedlist_page import LinkedListPage
from recursion_page import RecursionPage
from stack_page import StackPage

# --- Linked List Classes (Data Models) ---
class SLL_Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class SinglyLinkedList:
    def __init__(self, app):
        self.head = None
        self.app = app
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

class DLL_Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
class DoublyLinkedList:
    def __init__(self, app):
        self.head = None
        self.app = app
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

class CLL_Node: 
    def __init__(self, data):
        self.data = data
        self.next = None
class CircularLinkedList:
    def __init__(self, app):
        self.head = None
        self.app = app
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
    def __init__(self, parent, geometry="300x180", image_size=(100, 100), bg_color="#F0F0F0", fg_color="black"):
        tk.Toplevel.__init__(self, parent)
        self.title("Loading...")
        self.parent = parent
        self.frames = []
        self.frame_index = 0
        self.geometry_str = geometry
        self.image_size = image_size
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.pil_image = None # To store original PIL image for glitching
        self.is_glitching = False
        
        self.config(bg=self.bg_color)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.chosen_content = parent.chosen_splash_content
        content_path = os.path.join(script_dir, self.chosen_content)

        if self.chosen_content.endswith(".png"):
            self.handle_png(content_path, self.image_size)
        else:
            self.handle_gif(content_path, self.image_size)

    def handle_gif(self, gif_path, gif_size):
        """Loads and prepares an animated GIF."""
        try:
            self.gif_image = Image.open(gif_path)
            while True:
                resized_frame = self.gif_image.copy().resize(gif_size, Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(resized_frame))
                self.gif_image.seek(len(self.frames))
        except EOFError:
            pass
        except FileNotFoundError:
            self.create_error_placeholder(f"{os.path.basename(gif_path)} not found!")
        except Exception as e:
            self.create_error_placeholder(f"Error: {e}")

        if self.frames:
            self.setup_ui()
            self.frame_count = len(self.frames)
            if self.frame_count > 1:
                self.animate()

    def handle_png(self, png_path, png_size):
        """Loads and prepares a static PNG."""
        try:
            img = Image.open(png_path)
            self.pil_image = img.copy()
            resized_img = img.resize(png_size, Image.Resampling.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(resized_img))
        except FileNotFoundError:
            self.create_error_placeholder(f"{os.path.basename(png_path)} not found!")
        except Exception as e:
            self.create_error_placeholder(f"Error: {e}")
        
        if self.frames:
            self.setup_ui()
    
    def setup_ui(self):
        """Creates the common UI elements for the splash screen."""
        self.label = tk.Label(self, image=self.frames[0], bg=self.bg_color, bd=0)
        self.label.pack(padx=10, pady=(10, 5))
        self.group_label = tk.Label(
            self, 
            text="Group 6", 
            font=("Arial", 16, "bold"), 
            bg=self.bg_color, fg=self.fg_color
        )
        self.group_label.pack(pady=(0, 5))

        self.project_label = tk.Label(
            self, 
            text="Midterm Project", 
            font=("Arial", 12), 
            bg=self.bg_color, fg=self.fg_color
        )
        self.project_label.pack(pady=(0, 10))

        self.geometry(self.geometry_str)

        self.center_window()
        self.overrideredirect(True)

    def create_error_placeholder(self, error_text):
        """Creates a placeholder in case an image fails to load."""
        self.frames.append(ImageTk.PhotoImage(Image.new("RGB", (100, 100), "#F0F0F0")))
        self.setup_ui()
        self.label.config(text=error_text, image='', compound='center', height=6, width=20)

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
            delay = self.gif_image.info.get('duration', 90)
            if self.chosen_content == "teto.gif":
                delay = 50
        except AttributeError:
            delay = 100
        self.after(delay, self.animate)

    def shake(self, intensity=8):
        """
        Shakes the window. This should be called inside a loop
        or with `after` to create a continuous effect.
        """
        if not hasattr(self, 'original_x'):
            self.update_idletasks()
            self.original_x = self.winfo_x()
            self.original_y = self.winfo_y()

        dx = random.randint(-intensity, intensity)
        dy = random.randint(-intensity, intensity)
        self.geometry(f"+{self.original_x + dx}+{self.original_y + dy}")

    def reset_position(self):
        """Resets the window to its original centered position."""
        if hasattr(self, 'original_x'):
            self.geometry(f"+{self.original_x}+{self.original_y}")

    def glitch(self, probability=0.15, slice_height=10, max_offset=30):
        """
        Applies a glitch effect to the image by shifting a horizontal slice.
        """
        if self.is_glitching or not self.pil_image or random.random() > probability:
            return

        self.is_glitching = True

        glitched_img = self.pil_image.copy()
        width, height = glitched_img.size

        slice_y = random.randint(0, height - slice_height)
        slice_box = (0, slice_y, width, slice_y + slice_height)
        img_slice = glitched_img.crop(slice_box)


        offset = random.randint(-max_offset, max_offset)
        glitched_img.paste((0, 0, 0, 0), slice_box)
        glitched_img.paste(img_slice, (offset, slice_y))

        resized_glitch = glitched_img.resize(self.image_size, Image.Resampling.LANCZOS)
        self.glitched_frame = ImageTk.PhotoImage(resized_glitch)
        self.label.config(image=self.glitched_frame)

        self.after(random.randint(50, 100), self.reset_glitch)

    def reset_glitch(self):
        self.label.config(image=self.frames[0])
        self.is_glitching = False

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Linked List Visualizer")
        self.geometry("1000x650")
        self.chosen_splash_content = None
        self.withdraw()

        # --- Data Models (Shared) ---
        self.sll = SinglyLinkedList(self)
        self.dll = DoublyLinkedList(self)
        self.cll = CircularLinkedList(self)

        # --- Theme/Style Management ---
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
            "canvas_bg": "#3A3A3A", "node_fill": "#e67e22", "node_border": "white",
            "arrow_color": "white", "head_color": "lightgreen", "log_bg": "#1C1C1C", "log_fg": "white"
        }
        self.theme = self.light_theme

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.pages = {} # Dictionary to hold all page frames
        self.current_page_name = None # To track the active page

        self.log_text = None # Initialize log_text to None
        self.create_widgets()
        self.apply_theme(self.current_theme)
        
        # Start on the List page
        self.switch_page("list") 
        # self.log_output("Application started.") # Log is called in switch_page

    def create_widgets(self):
        self.vertical_paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.vertical_paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Top Frame (This is now just a container for the active page) ---
        self.top_frame_container = ttk.Frame(self.vertical_paned_window, style="Main.TFrame")
        self.vertical_paned_window.add(self.top_frame_container, weight=3)
        self.top_frame_container.grid_rowconfigure(0, weight=1)
        self.top_frame_container.grid_columnconfigure(0, weight=1)

        # --- Create all pages at startup and store them ---
        self.pages["list"] = LinkedListPage(self.top_frame_container, self)
        self.pages["recursion"] = RecursionPage(self.top_frame_container, self)
        self.pages["stack"] = StackPage(self.top_frame_container, self)


        # --- Bottom Frame (Log & Themes) ---
        self.bottom_frame = ttk.Frame(self.vertical_paned_window, style="Main.TFrame")
        self.vertical_paned_window.add(self.bottom_frame, weight=1)

        self.log_frame = ttk.LabelFrame(self.bottom_frame, text="Log-Output", padding=10, style="Log.TLabelframe")
        self.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        
        self.log_text = tk.Text(self.log_frame, height=8, state=tk.DISABLED, font=("Courier", 10), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_scroll = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.log_scroll.set)

        self.themes_frame = ttk.LabelFrame(self.bottom_frame, text="Themes", padding=10, style="Log.TLabelframe") # Corrected typo here
        self.themes_frame.pack(side=tk.RIGHT, padx=(5, 10), pady=10, fill=tk.Y)
        
        self.light_mode_btn = ttk.Button(self.themes_frame, text="Light Mode", command=lambda: self.apply_theme("light"))
        self.light_mode_btn.pack(pady=5, fill=tk.X)
        self.dark_mode_btn = ttk.Button(self.themes_frame, text="Dark Mode", command=lambda: self.apply_theme("dark"))
        self.dark_mode_btn.pack(pady=5, fill=tk.X)

    def switch_page(self, page_name):
        """Hides the current page and shows the selected one, preserving state."""
        
        # Hide the current page if it exists
        if self.current_page_name and self.current_page_name in self.pages:
            current_page = self.pages[self.current_page_name]
            current_page.grid_remove() # Hide it from view

        # Show the new page
        new_page = self.pages.get(page_name)
        if new_page:
            self.current_page_name = page_name
            new_page.grid(row=0, column=0, sticky="nsew")
            self.apply_theme_to_page() # Ensure theme is correct on switch

        if page_name == "list":
            self.log_output("Switched to List (Linked List) view.")
        elif page_name == "recursion":
            self.log_output("Switched to Recursion view.")
        elif page_name == "stack":
            self.log_output("Switched to Stack view.")

    def log_output(self, message):
        """Adds a message to the log output area."""
        if self.log_text:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def apply_theme(self, theme_name):
        """Applies the selected theme to all widgets."""
        if theme_name == "light":
            self.theme = self.light_theme
        elif theme_name == "dark":
            self.theme = self.dark_theme
        self.current_theme = theme_name

        self.config(bg=self.theme["bg"])

        self._configure_ttk_styles()
        self.log_text.config(bg=self.theme["log_bg"], fg=self.theme["log_fg"],
                              insertbackground=self.theme["fg"])
        self.apply_theme_to_page()
            
        self.log_output(f"Switched to {theme_name.capitalize()} Mode.")

    def apply_theme_to_page(self):
        """Helper function to apply theme to the current page if it exists."""
        pages_to_theme = self.pages.values() if not self.current_page_name else [self.pages[self.current_page_name]]
        for page in pages_to_theme:
            if hasattr(page, 'apply_theme'):
                page.apply_theme()

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

# --- Main execution ---
def main():
    available_content = ["loading.gif", "teto.gif", "phonk.gif"]
    chosen_content = random.choice(available_content)
    app = MainApp()
    app.chosen_splash_content = chosen_content
    if chosen_content == "phonk.gif":
        try:
            pygame.init()
            pygame.mixer.init()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            audio_path = os.path.join(script_dir, "phonk.mp3")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Audio Error: Could not play phonk.mp3. {e}")

        def show_phonk_splash():
            music_duration_before_fade = 5000 
            fadeout_time = 1000
            splash = SplashScreen(app, geometry="400x300", image_size=(200, 200),
                                  bg_color="#1C1C1C", fg_color="white")
            
            def update_splash_state():
                if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                    splash.shake()
                    splash.glitch()
                    app.after(50, update_splash_state)
                else:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop() 
                    splash.reset_position()
                    splash.destroy()
                    app.deiconify()
            app.after(50, update_splash_state)
            app.after(music_duration_before_fade, 
                      lambda: pygame.mixer.music.fadeout(fadeout_time))
            
        app.after(2000, show_phonk_splash)
    else: # Standard GIF behavior
        splash = SplashScreen(app) # Uses default geometry
        app.after(3000, lambda: (splash.destroy(), app.deiconify()))

    app.mainloop()

if __name__ == "__main__":
    main()
