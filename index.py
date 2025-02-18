class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book_name):
        """Adds a book to the library."""
        self.books.append({"name": book_name, "available": True})
        print(f'Book "{book_name}" added to the library.')

    def display_books(self):
        """Displays available books in the library."""
        print("\n📚 Available Books in the Library:")
        found = False
        for book in self.books:
            if book["available"]:
                print(f"- {book['name']}")
                found = True
        if not found:
            print("No books are currently available.")

    def borrow_book(self, book_name):
        """Allows a user to borrow a book."""
        for book in self.books:
            if book["name"].lower() == book_name.lower() and book["available"]:
                book["available"] = False
                print(f'✅ You have borrowed "{book_name}".')
                return
        print(f'❌ Sorry, "{book_name}" is not available.')

    def return_book(self, book_name):
        """Allows a user to return a borrowed book."""
        for book in self.books:
            if book["name"].lower() == book_name.lower() and not book["available"]:
                book["available"] = True
                print(f'🔄 You have returned "{book_name}". Thank you!')
                return
        print(f'⚠️ "{book_name}" was not borrowed from this library.')

# 📌 Main Program
library = Library()
library.add_book("The Great Gatsby")
library.add_book("Harry Potter")
library.add_book("Python Programming")

while True:
    print("\n📖 Library Menu")
    print("1. View Books")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        library.display_books()
    elif choice == "2":
        book_name = input("Enter the name of the book to borrow: ")
        library.borrow_book(book_name)
    elif choice == "3":
        book_name = input("Enter the name of the book to return: ")
        library.return_book(book_name)
    elif choice == "4":
        print("📚 Thank you for using the Library System. Goodbye!")
        break
    else:
        print("❌ Invalid choice. Please enter a number between 1-4.")
