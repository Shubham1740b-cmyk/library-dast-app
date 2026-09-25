"""
VIEWMODEL: Loan

Prepares data specifically for loan-related views.
Handles list operations and issue/return operations.
"""
from models.book import Book
from models.loan import Loan
from models.member import Member


class LoanViewModel:
    @staticmethod
    def get_loans_for_list():
        """Get list of loans for display in loan list view."""
        return Loan.all()
    
    @staticmethod
    def get_books_for_loan_dropdown():
        """Get list of books for loan issue dropdown."""
        return Book.all()
    
    @staticmethod
    def get_members_for_loan_dropdown():
        """Get list of members for loan issue dropdown."""
        return Member.all()
    
    @staticmethod
    def issue_book(book_id, member_id):
        """Issue a book and return (success, message) tuple."""
        return Loan.issue(book_id, member_id)
    
    @staticmethod
    def return_book(loan_id):
        """Return a book and return (success, message) tuple."""
        return Loan.return_book(loan_id)
