# Library System

## Introduction

This project is a comprehensive, command-line **Library System** built in Python. It provides a complete solution for managing a small personal or community library, including items like **Books**, **DVDs**, and **Magazines**.

The application features a fully interactive, menu-driven interface that does not require users to type commands. Instead, navigation is handled with keyboard arrows (`W/S` or `Up/Down`). Users can add new items, search the collection, view detailed information, and manage borrowing. All library data is persistently stored in a `JSON` file, ensuring that the state is saved between sessions.

---

## Features

### System & User Interface

- **Fully Interactive Menu:** Navigate using `W/S` or `Up/Down` arrow keys. Selections are made with `Enter` or `Space`.
- **Cross-Platform Compatibility:** Single-key input detection works on Windows (`msvcrt`), macOS, and Linux (`tty`, `termios`).
- **Coloured Terminal Output:** Uses the `colorama` library for colour-coded feedback. Available items show a green check (`✓`), unavailable items a red cross (`✕`), and messages are colour-coded.
- **Robust Data Handling:** Loads all data from `library_data.json` at startup, with error checking for corrupted data and duplicate Item IDs.
- **First-Run Setup:** If no data file is found, the system auto-populates with a "canned demo"-a predefined set of items-to showcase features.

### Item & Library Management

- **Add New Items:** Guided process for adding Books, DVDs, or Magazines, with input validation for numbers and dates.
- **View Item Details:** After searching, users can select an item to view its full, formatted details.
- **Comprehensive Listing:** List all items, only available items, or only borrowed items.
- **Borrow & Return Items:** Borrow and return items through an interactive selection menu.
- **Powerful Search:** Case-insensitive search by title or unique ID.

---

## Installation

1. **Ensure Python 3.6+ is installed** on your system.
2. **Clone the repository or download all `.py` files** into a single directory:
    ```sh
    git clone https://github.com/HeyCuby/Library-System.git
    cd Library-System
    ```
3. **Install the required external library**:
    ```sh
    pip install colourama
    ```

---

## How to Run the Program

1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Run the application:
    ```sh
    python main.py
    ```
4. The main menu will appear. Use `W/S` or `Up/Down` arrow keys to navigate. Press `Enter` or `Space` to select.

---

## Example Usage

A typical user session:

1. **Add a book:** Select "Add a New Item" and choose "Book". Enter Title, ID, Author, Page Count, and Genre.
2. **Success message:** "Successfully added 'New Book Title' to the library."
3. **Search for an item:** Select "Search for an Item" and enter a query (e.g., `Matrix`).
4. **View details:** Select a result to see details (e.g., "DVD: 'The Matrix' directed by Wachowskis | Duration: 136 min | ID: D001").
5. **Return to menu:** Press `Enter` to go back, or `q` to return to the main menu.

---

## Class Hierarchy & Inheritance

The system uses object-oriented programming with a clear class hierarchy:

```
LibraryItem
├── Book
├── DVD
└── Magazine
```
```

- **LibraryItem:** Base class with common attributes (`title`, `author`, `itemId`, `available`) and methods (`borrow_item`, `return_item`, `is_available`, `display_info`).
- **Book:** Adds `numPages` and `genre`.
- **DVD:** Adds `director` and `duration`.
- **Magazine:** Adds `issueNumber` and `publicationDate`.

Each subclass **overrides** `display_info()` to display type-specific details, demonstrating polymorphism.

> **Note:** Attribute names use `lowerCamelCase` (e.g., `itemId`, `numPages`) for consistency across all classes.

---

## Canned Demonstration

On first run (if `library_data.json` is missing), the system auto-populates with a set of demo items:
- Several Books, DVDs, and Magazines are added.
- Some items are pre-borrowed to demonstrate availability and borrowing features.
- The library’s state is displayed, showing available and borrowed items.

---

## Design Choices

- **Object-Oriented Programming (OOP):** Classes and inheritance provide clean separation of concerns. Overriding `display_info()` in each subclass is a prime example of polymorphism.
- **JSON for Data Persistence:** Lightweight, human-readable, and natively supported by Python. Data loading includes checks for duplicate IDs.
- **Modular UI Flows:** User interactions (adding items, viewing details) are encapsulated in dedicated functions, keeping the main loop clean.
- **Robust User Input Validation:** The `get_validated_input` function ensures correct data types (e.g., integer for pages, `YYYY-MM-DD` for dates).
- **Cross-Platform Input Handling:** OS checks ensure single-key input works on all platforms.

---

## Dependencies

### Built-in Modules

- `os`: Clears the console and checks OS name.
- `sys`: Accesses system-specific parameters for input.
- `json`: Encodes/decodes library data for persistent storage.
- `datetime`: Handles `publicationDate` in `Magazine`.
- `msvcrt`: (Windows only) Captures single key presses.
- `tty` & `termios`: (Unix-like only) Raw terminal access for key presses.

### External Modules

- `colorama`: Adds coloured text output to the terminal.

Install with:
```sh
pip install colorama
```

---

## Screenshots & Output Documentation

To fully demonstrate the system, include screenshots showing:
- Adding a new item
- Borrowing and returning items
- Listing available and borrowed items
- Searching and viewing item details

---