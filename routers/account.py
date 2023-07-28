from flask import Blueprint, session, request, render_template, flash, redirect
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

account_router = Blueprint(
    "account_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@account_router.route("/login", methods=["GET", "POST"])
def login_handler():
    if session.get("user_id", None):
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", None)
    password = request.form.get("password", None)
    if not email or not password:
        flash("You must provide your email and your password")
        return render_template("login.html")
    user = db.execute("SELECT * FROM users WHERE email LIKE ?;", email)
    if len(user) != 1 or not check_password_hash(user[0]["password"], password):
        flash("Wrong credentials")
        return render_template("login.html")
    session["user_id"] = user[0]["id"]
    session["is_admin"] = user[0]["is_admin"]
    return redirect("/")


@account_router.route("/register", methods=["GET", "POST"])
def registeration_handler():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", None)
    email = request.form.get("email", None)
    pass1 = request.form.get("pass1", None)
    pass2 = request.form.get("pass2", None)
    phone = request.form.get("phone", None)
    birthdate = request.form.get("birthdate", None)
    gender = request.form.get("gender", None)

    check_list = [name, email, pass1, pass2, phone, birthdate, gender]
    is_checked = all([bool(x) for x in check_list])
    if not is_checked:
        return render_template("register.html")

    if pass1 != pass2:
        flash("Passwords didn't match")
        return render_template("register.html")

    result = db.execute("SELECT * FROM users WHERE email = ?;", email)
    if len(result) == 1:
        flash("Email already used")
        return render_template("register.html")

    user_id = db.execute(
        "INSERT INTO users (name, email, password,phone,birthdate,gender) VALUES (?,?,?,?,?,?);",
        name,
        email,
        generate_password_hash(pass1),
        phone,
        birthdate,
        gender,
    )

    return redirect("/login")


@account_router.route("/logout")
def logout():
    session.clear()
    return redirect("/")
