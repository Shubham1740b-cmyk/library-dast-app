"""Application-wide settings. Deliberately kept outside the three MVVM layers."""

DATABASE = "library.db"
SECRET_KEY = "teaching-demo-key"

# --- Library identification -------------------------------------------
LIBRARY_NAME = "shubhamkumar's Library"  # Updated for assignment requirement

# --- Library business policy -------------------------------------------
LOAN_PERIOD_DAYS = 14      # how long a member may keep a book
MAX_BOOKS_PER_MEMBER = 3   # how many books one member may hold at once
FINE_PER_DAY = 5           # rupees charged for each day a book is late
