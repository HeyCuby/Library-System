# Library System - Andy Huang 26/07/2025

# Imports:
import os
# Allows access to the operating system
import sys
# Allows access to system parameters and functions
from datetime import date
# Used to work with dates, the 'date' object is used for the Magazine class
import json
# Used for encoding and decoding data into JSON format which would be used to save library data to a file
from colorama import Fore, Style, Back, init
# A third party library that allows for coloured terminal text and styling
try:
    import msvcrt
    # Microsoft Visual C++ Runtime. Contains functions for console I/O on Windows only
except ImportError:
    import tty
    import termios
    # These two lines would only be run if OS is not Windows and they allow for console I/O on other OS
init(autoreset=True)
# Initializes colorama
# autoreset is a setting that automatically calls Style.RESET_ALL after each print statement to prevent bleeding

# Import Classes:
from libraryItem import LibraryItem
from book import Book
from dvd import DVD
from magazine import Magazine

# Help Functions:

def clear_screen():
    """
    Clears the console screen.
    It checks the name of the operating system to use the correct command.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key():
    """
    Gets a single key press from the user without requiring them to press Enter.
    This function is platform dependent.
    """
    if os.name == 'nt':
        # Windows implementation:
        try:
            return msvcrt.getch().decode('utf-8')
            # msvcrt.getch() reads a single keypress and returns it as a byte string and .decode() converts it into a string
        except UnicodeDecodeError:
            return msvcrt.getch().decode('utf-8', errors='ignore')
            # Handles special keys that might not decode into utf-8
    else:
        # Unix-like (Linux, macOS) implementation:
        fd = sys.stdin.fileno()
        # Get the file descriptor for standard input
        old_settings = termios.tcgetattr(fd)
        # Store the original terminal settings so we can restore them later
        try:
            tty.setraw(sys.stdin.fileno())
            # tty.setraw() changes the terminal mode from "cooked" to "raw" which allows key pressed to be read instantly
            ch = sys.stdin.read(1)
            # Read a single character from standard input.
            if ch == '\x1b':
                ch += sys.stdin.read(2)
            # Arrow keys are sent as escape sequences (e.g., '\x1b[A' for Up)
            # If we detect an escape character, we read the next two characters to get the full sequence
        finally:
            # The 'finally' block ensures that the terminal settings are always restored to normal even if an error occurs
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

#  Library System Management:

class LibrarySystem:
    """
    Manages the entire collection of LibraryItem objects and user interactions.
    This class handles loading from and saving to a JSON file.
    """
    def __init__(self, data_file_path: str):
        """Initializes the LibrarySystem."""
        self._items = []
        # A list to hold all LibraryItem objects
        # The underscore prefix on '_items' indicates it is an internal-use variable
        self.data_file_path = data_file_path
        # The path to the JSON data file
        self._load_data() 
        # Attempt to load data from the file upon initialization in case of previous save

    def _load_data(self):
        """
        Loads the library items from the JSON data file.
        If the file doesn't exist, it does nothing, leaving the library empty.
        Includes checks for duplicate IDs.
        """
        try:
            with open(self.data_file_path, 'r') as f:
                items_data = json.load(f)
                loaded_ids = set() # Keep track of IDs we've already loaded
                for data in items_data:
                    item_id = data.get('itemId')
                    if item_id in loaded_ids:
                        print(Fore.RED + f"Warning: Duplicate itemId '{item_id}' found in data file. Skipping.")
                        continue # Skip this duplicate item

                    item_type = data.pop('type', None)
                    if not item_type:
                        print(Fore.RED + "Warning: Item data is missing 'type'. Skipping.")
                        continue

                    try:
                        if item_type == 'Book':
                            self._items.append(Book(**data))
                        elif item_type == 'Magazine':
                            data['publicationDate'] = date.fromisoformat(data['publicationDate'])
                            self._items.append(Magazine(**data))
                        elif item_type == 'DVD':
                            self._items.append(DVD(**data))
                        else:
                            print(Fore.YELLOW + f"Warning: Unknown item type '{item_type}' found. Skipping.")
                            continue
                        
                        loaded_ids.add(item_id) # Add the new ID to our set
                    except (TypeError, KeyError) as e:
                        print(Fore.RED + f"Error creating item from data: {data}. Missing or incorrect key: {e}. Skipping.")

        except FileNotFoundError:
            print(Fore.YELLOW + "Data file not found. Starting with an empty library.")
        except (json.JSONDecodeError, KeyError) as e:
            print(Fore.RED + f"Error reading data file: {e}. Starting with an empty library.")

    def _save_data(self):
        """
        Saves the current list of library items to the JSON data file.
        This method is called anytime an item is borrowed or returned.
        """
        serializable_items = []
        for item in self._items:
            item_data = item.__dict__.copy()
            item_data['type'] = type(item).__name__

            if isinstance(item, Magazine):
                item_data['publicationDate'] = item_data['publicationDate'].isoformat()
            serializable_items.append(item_data)
        
        with open(self.data_file_path, 'w') as f:
            json.dump(serializable_items, f, indent=4)

    def add_item(self, item: LibraryItem):
        """
        Adds a new item to the library, checking for duplicate IDs first.
        """
        if self._find_item_by_id(item.itemId):
            print(Fore.RED + f"Error: An item with ID '{item.itemId}' already exists.")
            return False
        
        self._items.append(item)
        self._save_data()
        print(Fore.GREEN + f"Successfully added '{item.title}' to the library.")
        return True

    def populate_with_initial_data(self):
        """Adds the default set of items to the library and saves it. Can also be referred to as 'canned demo'"""
        print("Populating library with initial items for the first time...")
        # A list of items to add. We use the add_item method to ensure no duplicates.
        initial_items = [
            Book("The Hobbit", "J.R.R. Tolkien", "B001", 310, "Fantasy"),
            Book("1984", "George Orwell", "B002", 328, "Dystopian"),
            Book("Dune", "Frank Herbert", "B003", 412, "Science Fiction"),
            Book("Foundation", "Isaac Asimov", "B004", 255, "Science Fiction"),
            Book("Brave New World", "Aldous Huxley", "B005", 311, "Dystopian"),
            DVD("The Matrix", "Wachowskis", 136, "D001"),
            DVD("Inception", "Christopher Nolan", 148, "D002"),
            DVD("The Lord of the Rings", "Peter Jackson", 201, "D003"),
            Magazine("National Geographic", 230, date(2023, 10, 1), "M001"),
            Magazine("Scientific American", 1089, date(2024, 1, 1), "M002"),
            Magazine("Time", 5221, date(2023, 12, 25), "M003")
        ]
        for item in initial_items:
            self._items.append(item) # Directly append here as we know they are unique
        
        print("\nDemonstrating a pre-borrowed item...")
        item1 = self._find_item_by_id("B002")
        if item1:
            item1.borrow_item()
        
        item2 = self._find_item_by_id("D003")
        if item2:
            item2.borrow_item()
        
        self._save_data()
        print(Fore.GREEN + "Initial library data has been created and saved.")

    def _find_item_by_id(self, item_id: str) -> LibraryItem | None:
        """A private helper method to find an item by its unique ID. Returns None if no items matches search ID"""
        for item in self._items:
            if item.itemId == item_id:
                return item # Return the found item object
        return None # Return None if no item matches the ID
    
    def get_available_items(self):
        """Returns a list of all items that are currently available."""
        return [item for item in self._items if item.is_available()]

    def get_borrowed_items(self):
        """Returns a list of all items that are currently not available."""
        return [item for item in self._items if not item.is_available()]

    def borrow_item(self, item_id: str):
        """Handles the process of borrowing an item and saves the new state."""
        item = self._find_item_by_id(item_id)
        if item:
            if item.borrow_item():
                self._save_data()
                return True
        else:
            print(Fore.RED + "Error: Item ID not found.")
        return False

    def return_item(self, item_id: str):
        """Handles the process of returning an item and saves the new state."""
        item = self._find_item_by_id(item_id)
        if item:
            item.return_item()
            self._save_data()
        else:
            print(Fore.RED + "Error: Item ID not found.")
            
    def search_item(self, query: str) -> list:
        """
        Searches for items by title or ID and returns a list of results.
        Returns an empty list if no items are found or the query is empty.
        """
        if not query:
            return [] # Return empty list if query is empty
        query = query.lower()
        results = [
            item for item in self._items 
            if query in item.title.lower() or query in item.itemId.lower()
        ]
        return results

    def _display_item_list(self, item_list: list):
        """
        A private helper method to display a list of items in a formatted, tree-like structure.
        """
        if not item_list:
            print("No items to display in this category.")
            return

        last_index = len(item_list) - 1
        for i, item in enumerate(item_list):
            prefix = "└── " if i == last_index else "├── "
            if item.is_available():
                status_display = f"[{Fore.GREEN}✓{Style.RESET_ALL}]" 
            else:
                status_display = f"[{Fore.RED}✕{Style.RESET_ALL}]"
            item_type = type(item).__name__
            item_details = f"'{item.title}' (ID: {item.itemId})"
            print(f"{prefix}{status_display} {item_type}: {item_details}")

    def list_all_items(self):
        """Displays all items in the library."""
        clear_screen()
        print("\n--- All Library Items ---")
        self._display_item_list(self._items)
        print("-------------------------")

    def list_available_items(self):
        """Displays only the available items."""
        clear_screen()
        print("\n--- Available Items ---")
        self._display_item_list(self.get_available_items())
        print("-----------------------")

    def list_borrowed_items(self):
        """Displays only the borrowed items."""
        clear_screen()
        print("\n--- Borrowed Items ---")
        self._display_item_list(self.get_borrowed_items())
        print("----------------------")

#  UI Functions:

def selection_menu(prompt: str, options: list):
    """
    Creates a reusable, interactive menu for selecting an option from a list.
    Returns the selected item, or None if the user cancels.
    """
    if not options:
        clear_screen()
        print(f"\n{prompt}")
        print(Fore.YELLOW + "No items to display in this category.")
        return None
    
    selected_index = 0
    while True:
        clear_screen()
        print(f"\n{prompt} (Press 'q' to cancel)")
        print("-" * (len(prompt) + 20))
        for i, item in enumerate(options):
            # Check if the item is a LibraryItem or just a string for generic menus
            if isinstance(item, LibraryItem):
                display_text = f"{type(item).__name__}: '{item.title}' (ID: {item.itemId})"
            else:
                display_text = str(item)

            if i == selected_index:
                print(f"> {Back.WHITE}{Fore.BLACK} {display_text} {Style.RESET_ALL}")
            else:
                print(f"  {display_text}")
        print("-" * (len(prompt) + 20))
        print("Use W/S or Arrow Keys to navigate, Enter to select.")

        key = get_key()
        if key in ('\x1b[A', 'w', 'W'):
            selected_index = (selected_index - 1) % len(options)
        elif key in ('\x1b[B', 's', 'S'):
            selected_index = (selected_index + 1) % len(options)
        elif key in ('q', 'Q'):
            return None
        elif key in ('\r', ' '):
            return options[selected_index]

def display_main_menu(options: list, selected_index: int):
    """Displays the main interactive menu."""
    clear_screen()
    print("\n===== Library Menu =====")
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"> {Back.WHITE}{Fore.BLACK} {option} {Style.RESET_ALL}")
        else:
            print(f"  {option}")
    print("========================")
    print("Use W/S or Arrow Keys to navigate, Enter to select.")

def get_validated_input(prompt: str, validation_type: type):
    """
    A robust function to get and validate user input.
    It loops until a valid input of the specified type is given.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print(Fore.RED + "Input cannot be empty. Please try again.")
            continue
        # Repeat until user provides a non-empty input
        if validation_type == int:
            try:
                return int(user_input)
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a whole number.")
        elif validation_type == date:
            try:
                return date.fromisoformat(user_input)
            except ValueError:
                print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD.")
        else: # Default to string
            return user_input

def view_details_flow(results: list[LibraryItem]):
    """
    Handles the UI flow for viewing details of items from a search result.
    """
    if not results:
        clear_screen()
        print("\n--- Search Results ---")
        print("No items found matching your query.")
        return

    while True:
        # The selection_menu will display the list of items
        item_to_view = selection_menu("Select an item to view details:", results)

        if not item_to_view:
            # User pressed 'q' to cancel and return to the main menu
            break

        # If an item was selected, display its details
        clear_screen()
        print(f"--- Details for '{item_to_view.title}' ---")
        # This method is defined in the imported LibraryItem class
        item_to_view.display_info()
        print("-" * (len(item_to_view.title) + 20))
        input("\nPress Enter to return to the search results...")
        # After pressing enter, the loop will continue, showing the results menu again

def add_item_flow(library: LibrarySystem):
    """Allows for adding new items to the library."""
    clear_screen()
    item_type_options = ["Book", "DVD", "Magazine"]
    item_type = selection_menu("Select the type of item to add:", item_type_options)
    # Use selection_menu to let the user choose the type of item they want to add

    if not item_type:
        print("Add item cancelled.")
        return
    # If the user cancels, exit the function

    clear_screen()
    print(f"--- Adding a new {item_type} ---")
    
    title = get_validated_input("Enter Title: ", str)
    itemId = get_validated_input("Enter unique Item ID: ", str)
    # Common attributes
    
    if library._find_item_by_id(itemId):
        print(Fore.RED + f"Error: An item with ID '{itemId}' already exists.")
        return
    # Check for duplicate ID

    if item_type == "Book":
        author = get_validated_input("Enter Author: ", str)
        numPages = get_validated_input("Enter Number of Pages: ", int)
        genre = get_validated_input("Enter Genre: ", str)
        new_item = Book(title, author, itemId, numPages, genre)
    elif item_type == "DVD":
        director = get_validated_input("Enter Director: ", str)
        duration = get_validated_input("Enter Duration (minutes): ", int)
        new_item = DVD(title, director, duration, itemId)
    elif item_type == "Magazine":
        issueNumber = get_validated_input("Enter Issue Number: ", int)
        publicationDate = get_validated_input("Enter Publication Date (YYYY-MM-DD): ", date)
        new_item = Magazine(title, issueNumber, publicationDate, itemId)
        # Adding specific attributes
    library.add_item(new_item)

#  Main:

def main():
    """The main function that runs the entire command-line application."""
    DATA_FILE = "library_data.json"
    library = LibrarySystem(DATA_FILE)
    clear_screen()
    
    if not library._items:
        library.populate_with_initial_data()
        print("-" * 30)
        input("Press Enter to start...")

    menu_options = [
        "List All Items",
        "List Available Items",
        "List Borrowed Items",
        "Borrow an Item",
        "Return an Item",
        "Search for an Item",
        "Add a New Item", # New option
        "Exit"
    ]
    selected_option = 0

    while True:
        display_main_menu(menu_options, selected_option)
        key = get_key()

        if key in ('\x1b[A', 'w', 'W'):
            selected_option = (selected_option - 1) % len(menu_options)
        elif key in ('\x1b[B', 's', 'S'):
            selected_option = (selected_option + 1) % len(menu_options)
        elif key in ('\r', ' '):
            choice = selected_option

            match choice:
                case 0:
                    library.list_all_items()
                case 1:
                    library.list_available_items()
                case 2:
                    library.list_borrowed_items()
                case 3:
                    available_items = library.get_available_items()
                    item_to_borrow = selection_menu("Select an item to borrow:", available_items)
                    if item_to_borrow:
                        library.borrow_item(item_to_borrow.itemId)
                    else:
                        clear_screen()
                        print("Borrowing cancelled.")
                case 4:
                    borrowed_items = library.get_borrowed_items()
                    item_to_return = selection_menu("Select an item to return:", borrowed_items)
                    if item_to_return:
                        library.return_item(item_to_return.itemId)
                    else:
                        clear_screen()
                        print("Return cancelled.")
                case 5:
                    clear_screen()
                    query = input("Enter title or Item ID to search for: ").strip()
                    search_results = library.search_item(query)
                    # The new flow handles displaying results and the details menu
                    view_details_flow(search_results)
                case 6: # Add a New Item
                    add_item_flow(library)
                case 7: # Exit
                    clear_screen()
                    print("Thank you for using the Library System. Goodbye!")
                    break
            input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    main()
# This line ensures that the main function is called when the script is run directly
