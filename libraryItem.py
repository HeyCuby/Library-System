from colorama import Fore

class LibraryItem:
    """
    A base class representing a generic item in the library.
    This class contains the common attributes and methods that all library items (Books, DVDs, etc.) will share.
    """
    def __init__(self, title: str, author: str, itemId: str, available: bool = True):
        self.title = title # The title
        self.author = author # The primary creator
        self.itemId = itemId # A unique identifier
        self.available = available # A boolean indicating if the item can be borrowed

    def __repr__(self):
        # Used for debugging by showing properties of an object
        status = "Available" if self.available else "Checked out"
        return f"<{self.__class__.__name__} {self.itemId}: {self.title!r} ({status})>"
    
    def display_info(self):
        """Prints a formatted string of the item's attributes."""
        kv_pairs = [f"{key}: {value}" for key, value in self.__dict__.items() if key != 'available']
        line = " | ".join(kv_pairs)
        print(f"| {line} |")
        # Creates key:value pairs in a list for all attributes in the object's dictionary except for 'available' and joins them into a single string separated by " | "
        # This is never used directly but can be useful for debugging

    def borrow_item(self):
        """Marks the item as borrowed. Returns a bool where 'True' indicates a sucessful borrow."""
        if not self.is_available():
            print(Fore.YELLOW + f"Sorry, '{self.title}' is currently unavailable.")
            return False
            # If the item is already checked out, inform the user and return False
        else:
            self.available = False
            print(Fore.GREEN + f"You have successfully borrowed '{self.title}'.")
            return True
            # If available, change its status, inform the user, and return True
    
    def return_item(self):
        """Marks the item as returned. Void function."""
        self.available = True
        print(Fore.GREEN + f"Thank you for returning '{self.title}'.")

    def is_available(self):
        """A simple method to check the availability status. Void function."""
        return self.available

