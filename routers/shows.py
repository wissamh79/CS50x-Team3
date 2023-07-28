from flask import Blueprint, session, request, render_template, flash, redirect
from database import db

shows_router = Blueprint(
    "shows_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@shows_router.route("/shows")
def list_shows(page_number=1, page_size=20):
    page_number = int(request.args.get("page_number", 1))
    page_size = int(request.args.get("page_size", 20))
    offset = (page_number - 1) * page_size
    result = db.execute(
        "SELECT * FROM shows ORDER BY release DESC LIMIT ? OFFSET ?;",
        page_size,
        offset,
    )
    return render_template("shows.html", shows=result)


@shows_router.route("/shows/<show_id>")
def show_details(show_id):
    try:
        show = db.execute("SELECT * FROM shows WHERE id=?;", show_id)[0]
    except:
        return render_template("404.html")

    return render_template("show_details.html", show=show)
