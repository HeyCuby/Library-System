# Library System

## Introduction

This project is a comprehensive, command-line **Library System** built in Python. It provides a complete solution for managing a small personal or community library, including items like **Books**, **DVDs**, and **Magazines**.

The application features a fully interactive, menu-driven interface that does not require users to type commands. Instead, navigation is handled with keyboard arrows. Users can add new items, search the collection, view detailed information, and manage borrowing. All library data is persistently stored in a `JSON` file, ensuring that the state is saved between sessions.

## Features

### System & User Interface
- **Fully Interactive Menu:** Navigate the system using `W/S` or `Up`/`Down` arrow keys. Selections are made with `Enter` or `Space`. This modern CLI approach provides a smooth user experience.
- **Cross-Platform Compatibility:** The system intelligently detects the operating system to provide single-key input detection on **Windows** (`msvcrt`), **macOS**, and **Linux** (`tty`, `termios`).
- **coloured Terminal Output:** Utilizes the `colourama` library to provide clear, colour-coded feedback. Available items are marked with a green check (`✓`), unavailable items with a red cross (`✕`), and success/error messages are coloured for readability.
- **Robust Data Handling:**
    - On startup, the system loads all data from `library_data.json`.
    - It now includes **error checking** for corrupted data, including handling of duplicate Item IDs to prevent crashes.
- **First-Run Setup:** If no `library_data.json` file is found, the application automatically populates itself with a "canned demo" - a predefined set of items - to showcase its features immediately.

### Item & Library Management
- **Add New Items:** A guided, step-by-step process allows users to add new Books, DVDs, or Magazines to the library. The system includes **input validation** to ensure data like numbers and dates are entered correctly.
- **View Item Details:** After searching for an item, users can select an item from the results to view its full, formatted details in a dedicated screen.
- **Comprehensive Listing:** Users can choose to list:
    - All items in the library.
    - Only items that are currently **available** to borrow.
    - Only items that have been **borrowed**.
- **Borrow & Return Items:** Items are borrowed and returned through a dedicated interactive selection menu, preventing invalid inputs.
- **Powerful Search:** A case-insensitive search allows users to find any item by querying its **title** or unique **ID**.

## Installation

1.  **Ensure Python 3.6+ is installed** on your system and accessible from the command line.
2.  **Clone the repository or download all `.py` files** into a single project directory.
    ```sh
    git clone https://github.com/HeyCuby/Library-System.git
    cd Library-System
    ```
3.  **Install the required external library** using the Python package installer, `pip`.
    ```sh
    pip install colourama
    ```

## How to Run the Program

1.  **Open your terminal or command prompt.**
2.  **Navigate to the directory** where you saved the project files.
3.  **Run the application** by executing the main script:
    ```sh
    python main.py
    ```
4.  The main menu will appear. Use the `W/S` or `Up`/`Down` arrow keys to navigate the options.
5.  Press `Enter` or `Space` to make a selection.

## Example Usage

A typical user session demonstrating the new features:

1.  **User wants to add a book.** They navigate to **"Add a New Item"** and press `Enter`.
2.  **The system asks for the item type.** The user selects **"Book"**.
3.  **The program prompts for details.** The user enters the Title, ID, Author, Page Count, and Genre, with the system validating the numerical input for pages.
4.  **A success message is displayed:** "Successfully added 'New Book Title' to the library." The data is saved.
5.  **User wants to find an item.** They select **"Search for an Item"** and enter the query `Matrix`.
6.  **The system shows a menu of search results:** "DVD: 'The Matrix' (ID: D001)".
7.  **The user selects the item** from the results menu to see more information.
8.  **A new screen appears,** displaying the formatted details: "DVD: 'The Matrix' directed by Wachowskis | Duration: 136 min | ID: D001".
9.  The user presses `Enter` to go back to the search results, and then `q` to return to the main menu.

## Class Hierarchy

The project's object-oriented structure is key to its functionality. The `LibraryItem` class is the foundation for all items.
```sh
LibraryItem
|
├── Book
├── DVD
└── Magazine
```

-   **`LibraryItem`**: The parent class. It defines core attributes (`title`, `itemId`, `available`) and methods (`borrow_item`, `return_item`). It also has a base `display_info()` method.
-   **`Book`**, **`DVD`**, **`Magazine`**: These subclasses inherit from `LibraryItem` and add their own unique attributes. Crucially, each of these classes **overrides** the `display_info()` method to provide a custom, formatted string of its specific details. This allows the "View Details" feature to show relevant information for each item type.

## Design Choices

Several key design decisions were made to ensure the program is robust, user-friendly, and maintainable.

-   **Object-Oriented Programming (OOP):** Using classes and inheritance allows for a clean separation of concerns. The new `display_info` override in each subclass is a prime example of polymorphism, allowing the same method call to behave differently based on the object type.
-   **JSON for Data Persistence:** JSON was chosen as it is lightweight, human-readable, and natively supported by Python. The new data loading logic includes checks for duplicate IDs, making the system more resilient to data corruption.
-   **Modular UI Flows:** Complex user interactions, like adding an item or viewing details, are encapsulated in their own functions (`add_item_flow`, `view_details_flow`). This keeps the main application loop clean and separates UI logic from core system management.
-   **Robust User Input Validation:** The `get_validated_input` function ensures that the user provides data in the correct format (e.g., an integer for page numbers, a `YYYY-MM-DD` string for dates). This prevents runtime errors and improves the user experience.
-   **Cross-Platform Input Handling:** The code explicitly checks the operating system (`os.name`) to import the correct library for single-key input. This was a crucial choice to ensure the core interactive functionality works consistently for all users.

## Dependencies

### Built-in Modules:
-   `os`: Used to clear the console screen and check the OS name.
-   `sys`: Used to access system-specific parameters and functions for non-Windows input.
-   `json`: Essential for encoding and decoding the library data for persistent storage.
-   `datetime`: Used for handling the `publicationDate` in the `Magazine` class.
-   `msvcrt`: (Windows only) Used for capturing single key presses.
-   `tty` & `termios`: (Unix-like only) Used for raw terminal access to capture single key presses.

### External Modules (install with pip):
-   `colourama`: Used for adding coloured text output to the terminal.

To install the necessary external dependency:
```sh
pip install colourama
