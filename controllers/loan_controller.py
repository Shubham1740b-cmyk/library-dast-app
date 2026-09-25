"""
CONTROLLER: Loans - MVVM Version

Issue and return books using ViewModel.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from viewmodels.loan_vm import LoanViewModel

loan_bp = Blueprint("loans", __name__, url_prefix="/loans")


@loan_bp.route("/")
def index():
    # Get all data needed for the loan list view from ViewModel
    return render_template(
        "loans/list.html",
        loans=LoanViewModel.get_loans_for_list(),
        books=LoanViewModel.get_books_for_loan_dropdown(),
        members=LoanViewModel.get_members_for_loan_dropdown()
    )


@loan_bp.route("/issue", methods=["POST"])
def issue():
    book_id = int(request.form["book_id"])
    member_id = int(request.form["member_id"])

    # Ask the ViewModel to issue the book (it delegates to the Model)
    ok, message = LoanViewModel.issue_book(book_id, member_id)
    # The controller reports the result
    flash(message, "success" if ok else "error")
    return redirect(url_for("loans.index"))


@loan_bp.route("/<int:loan_id>/return", methods=["POST"])
def give_back(loan_id):
    # Ask the ViewModel to return the book (it delegates to the Model)
    ok, message = LoanViewModel.return_book(loan_id)
    # The controller reports the result
    flash(message, "success" if ok else "error")
    return redirect(url_for("loans.index"))
