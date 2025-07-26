from datetime import date
from libraryItem import LibraryItem

class Magazine(LibraryItem):
    """Represents a magazine, inheriting from LibraryItem."""
    def __init__(self, title: str, issueNumber: int, publicationDate: date, itemId: str, author: str = "", available: bool = True):
        super().__init__(title, author, itemId, available)
        self.issueNumber = issueNumber
        self.publicationDate = publicationDate
        # Calls the __init__ method of LibraryItem and adds own class-specific attributes