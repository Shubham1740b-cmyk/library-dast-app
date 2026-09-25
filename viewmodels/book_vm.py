"""
VIEWMODEL: Book

Prepares data specifically for book-related views.
Handles both list and form operations.
"""
from models.book import Book


class BookViewModel:
    @staticmethod
    def get_books_for_list(search=None):
        """Get list of books for display in book list view."""
        return Book.all(search)
    
    @staticmethod
    def get_book_form_data():
        """Get empty form data for creating a new book."""
        return {
            'errors': [],
            'data': {
                'title': '',
                'author': '',
                'isbn': '',
                'copies': 1
            }
        }
    
    @staticmethod
    def validate_book_data(title, author, isbn, copies):
        """Validate book data and return ViewModel-ready format."""
        errors = Book.validate(title, author, isbn, copies)
        data = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'copies': copies
        }
        return {
            'errors': errors,
            'data': data
        }
    
    @staticmethod
    def create_book(title, author, isbn, copies):
        """Create a new book and return success message."""
        Book.create(title, author, isbn, copies)
        return f"'{title}' was added to the catalogue."
    
    @staticmethod
    def get_book_for_deletion(book_id):
        """Get book info for deletion confirmation."""
        return Book.find(book_id)
    
    @staticmethod
    def delete_book(book_id):
        """Delete a book."""
        Book.delete(book_id)
