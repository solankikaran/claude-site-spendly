import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, verify_user

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error=None, name="", email="")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = None
    if not name:
        error = "Name is required."
    elif not email or "@" not in email:
        error = "A valid email is required."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."

    if error:
        return render_template("register.html", error=error, name=name, email=email)

    if get_user_by_email(email):
        return render_template(
            "register.html",
            error="An account with that email already exists.",
            name=name,
            email=email,
        )

    new_user = create_user(name, email, password)
    session["user_id"] = new_user["id"]
    session["user_name"] = new_user["name"]
    flash("Welcome to Spendly!", "success")
    return redirect(url_for("landing"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None, email="")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = None
    if not email:
        error = "Email is required."
    elif not password:
        error = "Password is required."

    if not error:
        user = verify_user(email, password)
        if user is None:
            error = "Invalid email or password."

    if error:
        return render_template("login.html", error=error, email=email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    flash("Welcome back!", "success")
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
