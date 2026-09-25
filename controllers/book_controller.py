"""
CONTROLLER: Books - MVVM Version

List, search, add and remove books using ViewModel.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from viewmodels.book_vm import BookViewModel

book_bp = Blueprint("books", __name__, url_prefix="/books")


@book_bp.route("/")
def index():
    # 1. read the request
    search = request.args.get("q", "").strip()
    # 2. ask the ViewModel
    books = BookViewModel.get_books_for_list(search or None)
    # 3. choose a view and give it data
    return render_template("books/list.html", books=books, search=search)


@book_bp.route("/new")
def new():
    # Get empty form data from ViewModel
    form_data = BookViewModel.get_book_form_data()
    return render_template("books/form.html", errors=form_data['errors'], data=form_data['data'])


@book_bp.route("/", methods=["POST"])
def create():
    # 1. read the request
    title = request.form.get("title", "")
    author = request.form.get("author", "")
    isbn = request.form.get("isbn", "")
    copies = int(request.form.get("copies") or 0)

    # 2. let the ViewModel validate and prepare data
    vm_result = BookViewModel.validate_book_data(title, author, isbn, copies)
    if vm_result['errors']:
        # 3a. same view again, this time with the errors
        return render_template(
            "books/form.html", 
            errors=vm_result['errors'], 
            data=vm_result['data']
        )

    # 3b. success -> tell the ViewModel to save, then redirect
    message = BookViewModel.create_book(title, author, isbn, copies)
    flash(message, "success")
    return redirect(url_for("books.index"))


@book_bp.route("/<int:book_id>/delete", methods=["POST"])
def delete(book_id):
    book = BookViewModel.get_book_for_deletion(book_id)
    if book and book.issued_count > 0:
        flash("Cannot remove a book while copies are on loan.", "error")
    else:
        BookViewModel.delete_book(book_id)
        flash("Book removed from the catalogue.", "success")
    return redirect(url_for("books.index"))
