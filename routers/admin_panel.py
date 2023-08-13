from flask import Blueprint, session, request, render_template, flash, redirect
from database import db
import requests

admin_router = Blueprint(
    "admin_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates/",
)
## events

@admin_router.route("/events")
def admin_events_list():
    events = db.execute("SELECT * FROM events;")
    return render_template("admin/events/events_list.html", events=events)


@admin_router.route("/events/add", methods=["GET", "POST"])
def admin_events():
    if request.method == "GET":
       

        return render_template(
            "admin/events/event_add.html"
        )
    else:
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        is_featured = True if request.form.get("is_featured") == "on" else False
        poster = request.files.get("poster", None)


        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"poster": poster},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            poster = data["data"]["url"]
        else:
            poster = ""
        # Insert events table information
        event_id = db.execute(
            """
                   INSERT INTO events 
                   (title, description, date, is_featured, poster)
                   """,
            title,
            description,
            date,
            bool(is_featured),
            poster,
        )

        return redirect("/admin/events")


@admin_router.route("/events/<event_id>/edit", methods=["GET", "POST"])
def admin_events_edit(event_id):
    if request.method == "GET":
        try:
            event = db.execute("SELECT * FROM events WHERE id=?;", event_id)[0]
        except:
            return render_template("404.html")

        return render_template(
            "admin/events/event_edit.html",
            event=event,
        )

    # Post Method
    else:
        title = request.form.get("title")
        date = request.form.get("date")
        description = request.form.get("description")
        is_featured = True if request.form.get("is_featured") == "on" else False
        poster = request.files.get("poster", None)

        # If changed poster, Upload new poster.
        if poster:
            res = requests.post(
                "https://api.imgbb.com/1/upload",
                files={"poster": poster},
                params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
            )
            if res.ok:
                data = res.json()
                poster = data["data"]["url"]
        else:
            poster = db.execute("SELECT poster FROM events WHERE id=?", event_id)[0][
                "poster"
            ]
            
        # Start updating
        db.execute(
            """
                   UPDATE events SET title = ?, description = ?, date = ? , poster = ?, is_featured = ? WHERE id = ?;
                   """,
            title,
            description,
            date,
            poster,
            bool(is_featured),
            event_id,
        )

        return redirect("/admin/events")


## users

@admin_router.route("/users")
def admin_users_list():
    users = db.execute("SELECT * FROM users;")
    return render_template("admin/users/users_list.html", users=users)


@admin_router.route("/users/add", methods=["GET", "POST"])
def admin_users():
    if request.method == "GET":
       

        return render_template(
            "admin/users/user_add.html"
        )
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        birthday = request.form.get("birthday")
        is_featured = True if request.form.get("is_featured") == "on" else False


        # Insert users table information
        user_id = db.execute(
            """
                   INSERT INTO users 
                   (name, email, password, phone, birthday, is_featured)
                   """,
            name,
            email,
            password,
            phone,
            birthday,
            bool(is_featured),
        )

        return redirect("/admin/users")


@admin_router.route("/users/<user_id>/edit", methods=["GET", "POST"])
def admin_users_edit(user_id):
    if request.method == "GET":
        try:
            user = db.execute("SELECT * FROM users WHERE id=?;", user_id)[0]
        except:
            return render_template("404.html")

        return render_template(
            "admin/users/user_edit.html",
            user=user,
        )

    # Post Method
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        passowrd = request.form.get("passowrd")
        phone = request.form.get("phone")
        birthday = request.form.get("birthday")
        

        is_featured = True if request.form.get("is_featured") == "on" else False
  
        # Start updating
        db.execute(
            """
                   UPDATE users SET name = ?, email = ?, passowrd = ? , phone = ?, birthday = ?, is_featured = ? WHERE id = ?;
                   """,
            name,
            email,
            passowrd,
            phone,
            birthday,
            bool(is_featured),
            user_id,
        )

        return redirect("/admin/users")