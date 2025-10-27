# Discrete-Structure-Project

This project is a Python-based GUI application built with `tkinter` that visually demonstrates fundamental discrete data structures and concepts. It provides an interactive way to understand the operations of Linked Lists (Singly, Doubly, Circular), Stacks, and Recursion.

## Features

*   **Linked List Visualization:**
    *   Interactive representation of Singly, Doubly, and Circular Linked Lists.
    *   Operations: Append, Prepend, Delete, Add Random Node, and Reverse.
    *   Dynamic drawing of nodes and pointers.

*   **Stack Visualization:**
    *   LIFO (Last-In, First-Out) stack implementation.
    *   Operations: Push, Pop, Peek, Search, and display current size.
    *   Visual representation of stack elements with capacity indication.
    *   Custom error handling for Stack Overflow and Underflow with visual cues.

*   **Recursion Visualization:**
    *   Simulates and visualizes the call stack for Tail and Head recursion.
    *   Helps understand how function calls are managed on the stack during recursive processes.

*   **Theming:**
    *   Toggle between Light and Dark modes for a personalized experience.

*   **Activity Log:**
    *   A real-time log panel to track all user actions and system outputs.

*   **Dynamic Splash Screen:**
    *   Features a randomized splash screen on startup, including animated GIFs and special effects (like shake, glitch, and background music for specific content).

## Installation

To run this application, you need Python 3 installed on your system.

1.  **Clone the repository (if applicable) or download the project files.**

2.  **Navigate to the project directory:**

    ```bash
    cd Discrete-Structure-Project
    ```

3.  **Install the required Python packages using pip:**

    ```bash
    pip install Pillow pygame
    ```

    *   `Pillow`: Used for image processing (GIFs, PNGs) in the splash screen and error pop-ups.
    *   `pygame`: Used for playing audio in the splash screen (specifically for the "phonk.gif" option).

    *Note: `tkinter`, `ttk`, `os`, `time`, and `random` are standard Python libraries and do not require separate installation.*

## How to Run

After installing the dependencies, you can run the application by executing the `main.py` file:

```bash
python main.py
```

The application will launch with a splash screen, followed by the main GUI where you can explore the different data structures.
