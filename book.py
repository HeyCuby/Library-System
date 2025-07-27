from libraryItem import LibraryItem

class Book(LibraryItem):
    """Represents a book, inheriting from LibraryItem."""
    def display_info(self):
        print(f"Book: '{self.title}' by {self.author} | Pages: {self.numPages} | Genre: {self.genre} | ID: {self.itemId}")
        # Prints the attirbutes of the book in a formatted string
    def __init__(self, title: str, author: str, itemId: str, numPages: int, genre: str, available: bool = True):
        super().__init__(title, author, itemId, available)
        self.numPages = numPages
        self.genre = genre
        # Calls the __init__ method of LibraryItem and adds own class-specific attributes