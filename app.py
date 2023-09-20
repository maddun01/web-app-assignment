from flask import render_template
from web_application import app


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
