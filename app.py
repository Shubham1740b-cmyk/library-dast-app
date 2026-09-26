"""
Library Management System - entry point.

This file does one job: it builds the application and connects the three
MVVM layers together. It is the only place that knows about all of them.

    MODEL       models/       data + business rules
    VIEW        views/        Jinja2 templates + CSS
    VIEWMODEL   viewmodels/   prepares data for views
    CONTROLLER  controllers/  HTTP request handlers that use ViewModels
"""
from flask import Flask

import config
from controllers.book_controller import book_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.loan_controller import loan_bp
from controllers.member_controller import member_bp
from models.database import init_schema


def create_app():
    app = Flask(
        __name__,
        template_folder="views/templates",   # <- the VIEW layer lives here
        static_folder="views/static",
    )
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["LIBRARY_NAME"] = config.LIBRARY_NAME
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Make library name available to all templates
    @app.context_processor
    def inject_library_name():
        return dict(library_name=app.config["LIBRARY_NAME"])

    # register the CONTROLLER layer
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(loan_bp)

    init_schema()                            # make sure the MODEL has tables

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", debug=True, port=5000)