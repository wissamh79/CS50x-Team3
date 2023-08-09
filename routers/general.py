from flask import Blueprint, render_template, request, redirect, session
from database import db

general_router = Blueprint(
    "general_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates/",
)


@general_router.get("/")
def index():
    featured_events = db.execute(
        "SELECT * FROM Events WHERE is_featured = True;")

    events = db.execute("SELECT * FROM Events ORDER BY title DESC LIMIT 10;")

    data = {
        "featured_events": featured_events,

        "events": events,

    }
    return render_template("index.html", data=data)
