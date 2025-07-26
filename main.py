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

#  Library System Management:

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
        """
        try:
            with open(self.data_file_path, 'r') as f:
                # Open the file in read mode
                items_data = json.load(f)
                # Load the list of item dictionaries from the JSON file
                for data in items_data:
                    item_type = data.pop('type')
                    # Iterate through each dictionary in the loaded list and gets the item's type ("Book", "DVD")
                    if item_type == 'Book':
                        self._items.append(Book(**data))
                        # The '**' unpacks the dictionary for automatic assignement of parameters
                    elif item_type == 'Magazine':
                        data['publicationDate'] = date.fromisoformat(data['publicationDate'])
                        self._items.append(Magazine(**data))
                        # Converting date from string back to date format
                        # The '**' unpacks the dictionary for automatic assignement of parameters
                    elif item_type == 'DVD':
                        self._items.append(DVD(**data))
                        # The '**' unpacks the dictionary for automatic assignement of parameters
        except FileNotFoundError:
            # If the file does not exist, the library will start empty, and the file will be created on the first save
            print(Fore.YELLOW + "Data file not found. Starting with an empty library.")
        except (json.JSONDecodeError, KeyError) as e:
            # Handle cases where the file is corrupted or has incorrect data
            print(Fore.RED + f"Error reading data file: {e}. Starting with an empty library.")

    def _save_data(self):
        """
        Saves the current list of library items to the JSON data file.
        This method is called anytime an item is borrowed or returned.
        """
        serializable_items = []
        # A list to hold dictionaries that are safe to serialize into JSON
        for item in self._items:
            item_data = item.__dict__.copy()
            item_data['type'] = type(item).__name__
            # Copy the object's dictionary and add a 'type' key to save object type for next load

            if isinstance(item, Magazine):
                item_data['publicationDate'] = item_data['publicationDate'].isoformat()
                # If the object is a Magazine, convert the date to ISO format string (YYYY-MM-DD) which is a standard, JSON-compatible format
            serializable_items.append(item_data)
        
        # Open the data file in ('w')rite mode , which overwrites the existing contents
        with open(self.data_file_path, 'w') as f:
            # Use json.dump to write the list of dictionaries to the file
            # indent=4 makes the JSON file readable for users
            json.dump(serializable_items, f, indent=4)

    def populate_with_initial_data(self):
        """Adds the default set of items to the library and saves it. Can also be referred to as 'canned demo'"""
        print("Populating library with initial items for the first time...")
        # Add a variety of items to the library for demonstration
        self._items.append(Book("The Hobbit", "J.R.R. Tolkien", "B001", 310, "Fantasy"))
        self._items.append(Book("1984", "George Orwell", "B002", 328, "Dystopian"))
        self._items.append(Book("Dune", "Frank Herbert", "B003", 412, "Science Fiction"))
        self._items.append(Book("Foundation", "Isaac Asimov", "B004", 255, "Science Fiction"))
        self._items.append(Book("Brave New World", "Aldous Huxley", "B005", 311, "Dystopian"))
        self._items.append(DVD("The Matrix", "Wachowskis", 136, "D001"))
        self._items.append(DVD("Inception", "Christopher Nolan", 148, "D002"))
        self._items.append(DVD("The Lord of the Rings", "Peter Jackson", 201, "D003"))
        self._items.append(Magazine("National Geographic", 230, date(2023, 10, 1), "M001"))
        self._items.append(Magazine("Scientific American", 1089, date(2024, 1, 1), "M002"))
        self._items.append(Magazine("Time", 5221, date(2023, 12, 25), "M003"))
        
        print("\nDemonstrating a pre-borrowed item...")
        # Pre-borrow some items to show how borrowed lists work from the start
        item1 = self._find_item_by_id("B002")
        if item1:
            item1.borrow_item()
        
        item2 = self._find_item_by_id("D003")
        if item2:
            item2.borrow_item()
        
        self._save_data()
        print(Fore.GREEN + "Initial library data has been created and saved.")
        # Save this initial state to the data file.

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
            # If item is found
            if item.borrow_item():
                # If borrowing was successful, save the changes to the file
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
            # If item is found, return item and save file
        else:
            print(Fore.RED + "Error: Item ID not found.")
            
    def search_item(self, query: str):
        """Searches for items by title or ID and displays the results."""
        query = query.lower() # Convert query to lowercase for case insensitive search
        results = [
            item for item in self._items 
            if query in item.title.lower() or query in item.itemId.lower()
        ]
        # Create a list of items where the query is found in the title or itemId
        clear_screen()
        print("\n--- Search Results ---")
        if not results:
            print("No items found matching your query.")
        else:
            self._display_item_list(results)
            # Use the dedicated display method to show the results
        print("--------------------")

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
            # The prefix creates the "tree" look. '└──' for the last item, '├──' for others
            if item.is_available():
                status_display = f"[{Fore.GREEN}✓{Style.RESET_ALL}]" 
            else:
                status_display = f"[{Fore.RED}✕{Style.RESET_ALL}]"
            # Set the status symbol and color based on availability
            item_type = type(item).__name__ # Get the class name (e.g., "Book")
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

#  UI Functions:

def selection_menu(prompt: str, options: list[LibraryItem]):
    """
    Creates a reusable, interactive menu for selecting a library item from a list.
    Returns the selected item object, or None if the user cancels by pressing 'q'.
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
        # Prints a horizontal line the length of the prompt
        for i, item in enumerate(options):
            display_text = f"{type(item).__name__}: '{item.title}' (ID: {item.itemId})"
            # Saves the object's type, title, and ID for displaying
            if i == selected_index:
                print(f"> {Back.WHITE}{Fore.BLACK} {display_text} {Style.RESET_ALL}")
                # Highlight the currently selected item
            else:
                print(f"  {display_text}")
        print("-" * (len(prompt) + 20))
        print("Use W/S or Arrow Keys to navigate, Enter to select.")

        key = get_key()
        # Wait for a single key press

        # Update the selected_index based on user input.
        if key in ('\x1b[A', 'w', 'W'): # Up arrow or W
            # The modulo operator (%) ensures the selection wraps around correctly
            selected_index = (selected_index - 1) % len(options)
        elif key in ('\x1b[B', 's', 'S'): # Down arrow or S
            selected_index = (selected_index + 1) % len(options)
        elif key in ('q', 'Q'): # Quit option
            return None
        elif key in ('\r', ' '): # Enter or Space key confirms selection
            return options[selected_index]

def display_main_menu(options: list, selected_index: int):
    """Displays the main interactive menu."""
    clear_screen()
    print("\n===== Library Menu =====")
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"> {Back.WHITE}{Fore.BLACK} {option} {Style.RESET_ALL}")
            # Highlight the selected option with a background color
        else:
            print(f"  {option}")
    print("========================")
    print("Use W/S or Arrow Keys to navigate, Enter to select.")



#  Main:

def main():
    """The main function that runs the entire command-line application."""
    DATA_FILE = "library_data.json"
    # Define the name for our data file.

    library = LibrarySystem(DATA_FILE)
    # Create an instance of the library system, which will automatically try to load data from the provided file
    clear_screen()
    
    # Check if the library is empty after trying to load. If so, it's the first run
    if not library._items:
        library.populate_with_initial_data()
        print("-" * 30)
        input("Press Enter to start...")

    # Define the menu options and the initial selected position
    menu_options = [
        "List All Items",
        "List Available Items",
        "List Borrowed Items",
        "Borrow an Item",
        "Return an Item",
        "Search for an Item",
        "Exit"
    ]
    selected_option = 0
    # Sets the selection option to first (top) option

    while True:
        display_main_menu(menu_options, selected_option)
        key = get_key()
        # Display the menu and wait for the user to navigate or select

        # Update menu navigation based on key press
        if key in ('\x1b[A', 'w', 'W'): # Up
            selected_option = (selected_option - 1) % len(menu_options)
        elif key in ('\x1b[B', 's', 'S'): # Down
            selected_option = (selected_option + 1) % len(menu_options)
        elif key in ('\r', ' '): # Select (Enter or Space)
            choice = selected_option

            # Execute the corresponding action based on the user's choice
            match choice:
                case 0: # List all items
                    library.list_all_items()
                case 1: # List available items
                    library.list_available_items()
                case 2: # List borrowed items
                    library.list_borrowed_items()
                case 3: # Borrow an item
                    available_items = library.get_available_items()
                    item_to_borrow = selection_menu("Select an item to borrow:", available_items)
                    if item_to_borrow:
                        # If the user didnt cancel
                        library.borrow_item(item_to_borrow.itemId)
                    else:
                        clear_screen()
                        print("Borrowing cancelled.")
                case 4: # Return an Item
                    borrowed_items = library.get_borrowed_items()
                    item_to_return = selection_menu("Select an item to return:", borrowed_items)
                    if item_to_return:
                        # If the user didnt cancel
                        library.return_item(item_to_return.itemId)
                    else:
                        clear_screen()
                        print("Return cancelled.")
                case 5: # Search for an item
                    clear_screen()
                    query = input("Enter title or Item ID to search for: ").strip()
                    library.search_item(query)
                case 6: # Exit
                    clear_screen()
                    print("Thank you for using the Library System. Goodbye!")
                    break # Break out of the while loop to end the program
            input("\nPress Enter to return to the menu...")
            # Pause the screen until the user is ready to return to the menu

# This standard Python construct ensures that the main() function is called only when the script is executed directly (not when it's imported as a module)
if __name__ == "__main__":
    main()