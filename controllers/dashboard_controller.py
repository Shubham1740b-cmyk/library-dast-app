"""
CONTROLLER: Dashboard - MVVM Version

A controller is a thin coordinator. In MVVM:
    1. take the request        2. ask the ViewModel
    3. choose a template       4. hand it the data
There is no SQL here and no HTML here.
"""
from flask import Blueprint, render_template

from viewmodels.dashboard_vm import DashboardViewModel

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


@dashboard_bp.route("/")
def index():
    # Get all data from the ViewModel
    vm_data = DashboardViewModel.get_dashboard_data()
    return render_template("dashboard.html", **vm_data)
