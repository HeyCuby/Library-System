from datetime import date
from libraryItem import LibraryItem

class Magazine(LibraryItem):
    """Represents a magazine, inheriting from LibraryItem."""
    def display_info(self):
        print(f"Magazine: '{self.title}' | Issue: {self.issueNumber} | Date: {self.publicationDate} | ID: {self.itemId}")
        # Prints the attributes of the magazine in a formatted string
    def __init__(self, title: str, issueNumber: int, publicationDate: date, itemId: str, author: str = "", available: bool = True):
        super().__init__(title, author, itemId, available)
        self.issueNumber = issueNumber
        self.publicationDate = publicationDate
        # Calls the __init__ method of LibraryItem and adds own class-specific attributes