# Library System

## Introduction

This project is a comprehensive, command-line **Library System** built in Python. It provides a complete solution for managing a small personal or community library, including items like **Books**, **DVDs**, and **Magazines**.

The application features a fully interactive, menu-driven interface that does not require users to type commands. Instead, navigation is handled with keyboard arrows. All library data, including item details and borrowing status, is persistently stored in a `JSON` file, ensuring that the state is saved between sessions. Its object-oriented design makes it robust and easy to extend with new types of library items.

## Features

### System & User Interface
- **Fully Interactive Menu:** Navigate the system using `W/S` or `Up`/`Down` arrow keys. Selections are made with `Enter` or `Space`. This modern CLI approach provides a smooth user experience.
- **Cross-Platform Compatibility:** The system intelligently detects the operating system to provide single-key input detection on **Windows** (`msvcrt`), **macOS**, and **Linux** (`tty`, `termios`).
- **Colored Terminal Output:** Utilizes the `colorama` library to provide clear, color-coded feedback. Available items are marked with a green check (`✓`), unavailable items with a red cross (`✕`), and success/error messages are colored for readability.
- **Automatic Data Persistence:** On startup, the system loads all data from `library_data.json`. Any changes (borrowing, returning) are automatically saved back to the file, ensuring data integrity.
- **First-Run Setup:** If no `library_data.json` file is found, the application automatically populates itself with a "canned demo"—a predefined set of books, DVDs, and magazines—to showcase its features immediately.

### Item & Library Management
- **Object-Oriented Structure:** A base `LibraryItem` class provides core functionality, which is extended by specific classes for `Book`, `DVD`, and `Magazine`, each with their own unique attributes.
- **View Items:** Users can choose to list:
    - All items in the library.
    - Only items that are currently **available** to borrow.
    - Only items that have been **borrowed**.
- **Borrow & Return Items:**
    - Items are borrowed and returned through a dedicated interactive selection menu, preventing invalid inputs.
    - The system prevents users from borrowing an item that is already checked out.
- **Search Functionality:** A case-insensitive search allows users to find any item by querying its **title** or unique **ID**. Results are displayed in a clean, formatted list.

## Installation

1.  **Ensure Python 3.6+ is installed** on your system and accessible from the command line.
2.  **Clone the repository or download all `.py` files** into a single project directory.
    ```sh
    git clone https://github.com/HeyCuby/Library-System.git
    cd Library-System
    ```
3.  **Install the required external library** using the Python package installer, `pip`.
    ```sh
    pip install colorama
    ```

## How to Use

1.  **Run the application** by executing the main script from your terminal:
    ```sh
    python main.py
    ```
2.  **Navigate the main menu** using `W/S` or the `Up`/`Down` arrow keys. The currently selected option will be highlighted.
3.  **Press `Enter` or `Space`** to select an option from the menu.
4.  **For borrowing or returning**, a second interactive menu will appear, listing only the relevant items (e.g., only available items can be borrowed). Use the same keys to navigate and select. You can press `q` to cancel and return to the main menu.
5.  After viewing a list or performing an action, **press `Enter` to return to the main menu**.
6.  To exit the application, select the **"Exit"** option from the main menu.

## Project Structure

The project is logically divided into multiple files, each representing a key component of the system.

-   `main.py`: The main entry point. It contains the `LibrarySystem` class, which orchestrates all library operations, and the UI functions for displaying menus.
-   `libraryItem.py`: Defines the base `LibraryItem` class. It includes shared attributes (`title`, `itemId`, `available`) and methods (`borrow_item`, `return_item`).
-   `book.py`: Defines the `Book` class, which inherits from `LibraryItem` and adds `numPages` and `genre` attributes.
-   `dvd.py`: Defines the `DVD` class, inheriting from `LibraryItem` and adding `director` and `duration` attributes.
-   `magazine.py`: Defines the `Magazine` class, inheriting from `LibraryItem` and adding `issueNumber` and `publicationDate` attributes.

## Dependencies

### Built-in Modules:
-   `os`: Used to clear the console screen (`os.system`) and check the OS name.
-   `sys`: Used to access system-specific parameters and functions, primarily for non-Windows input.
-   `json`: Essential for encoding and decoding the library data for persistent storage in `library_data.json`.
-   `datetime`: Used specifically for handling the `publicationDate` in the `Magazine` class.
-   `msvcrt`: (Windows only) Used for capturing single key presses without requiring the Enter key.
-   `tty` & `termios`: (Unix-like only) Used for raw terminal access to capture single key presses.

### External Modules (install with pip):
-   `colorama`: Used for adding colored text output to the terminal, enhancing user feedback.

To install the necessary external dependency:
```sh
pip install colorama
