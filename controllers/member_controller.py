"""
CONTROLLER: Members - MVVM Version

List and register library members using ViewModel.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from viewmodels.member_vm import MemberViewModel

member_bp = Blueprint("members", __name__, url_prefix="/members")


@member_bp.route("/")
def index():
    # Get members and form data from ViewModel
    members = MemberViewModel.get_members_for_list()
    form_data = MemberViewModel.get_member_form_data()
    return render_template("members/list.html", members=members, errors=form_data['errors'], data=form_data['data'])


@member_bp.route("/", methods=["POST"])
def create():
    # 1. read the request
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    roll_no = request.form.get("roll_no", "")

    # 2. let the ViewModel validate and prepare data
    vm_result = MemberViewModel.validate_member_data(name, email, roll_no)
    if vm_result['errors']:
        # 3a. same view again, this time with the errors
        members = MemberViewModel.get_members_for_list()
        return render_template(
            "members/list.html", 
            members=members,
            errors=vm_result['errors'], 
            data=vm_result['data']
        )

    # 3b. success -> tell the ViewModel to save, then redirect
    message = MemberViewModel.create_member(name, email, roll_no)
    flash(message, "success")
    return redirect(url_for("members.index"))
