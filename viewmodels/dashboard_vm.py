"""
VIEWMODEL: Dashboard

Prepares data specifically for the dashboard view.
This is the ONLY place that knows how to combine data from multiple models
for the dashboard presentation.
"""
from models.book import Book
from models.loan import Loan
from models.member import Member


class DashboardViewModel:
    @staticmethod
    def get_dashboard_data():
        """Get all data needed for the dashboard view."""
        return {
            'books': Book.stats(),           # {'titles': X, 'copies': Y, 'available': Z}
            'members': Member.count(),       # integer
            'loans': Loan.stats(),           # {'on_loan': X, 'overdue': Y, 'fines_due': Z}
            'recent': Loan.active()[:5]      # list of Loan objects (max 5)
        }
