"""Main file for the application."""

## Consult the README for instructions

from flask import render_template
from web_application import app


@app.route("/")
def index():
    """Return template to display on startup."""
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=False)
