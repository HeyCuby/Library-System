from libraryItem import LibraryItem

class DVD(LibraryItem):
    """Represents a DVD, inheriting from LibraryItem."""
    def display_info(self):
        print(f"DVD: '{self.title}' directed by {self.director} | Duration: {self.duration} min | ID: {self.itemId}")
        # Prints the attributes of the DVD in a formatted string
    def __init__(self, title: str, director: str, duration: int, itemId: str, author: str = "", available: bool = True):
        super().__init__(title, director, itemId, available)
        self.director = director
        self.duration = duration # Duration in minute
        # Calls the __init__ method of LibraryItem and adds own class-specific attributes. Note that 'author' parameter is mapped to 'director'