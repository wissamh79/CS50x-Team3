from flask import Blueprint, session, request, render_template, flash, redirect
from database import db

events_router = Blueprint(
    "events_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@events_router.route("/events")
def list_events(page_number=1, page_size=20):
    page_number = int(request.args.get("page_number", 1))
    page_size = int(request.args.get("page_size", 20))
    offset = (page_number - 1) * page_size
    result = db.execute(
        "SELECT * FROM events ORDER BY title DESC LIMIT ? OFFSET ?;",
        (page_size, offset),  # Pass parameters as a tuple
    )
    return render_template("events.html", events=result)


@events_router.route("/events/<event_id>")
def event_details(event_id):
    try:
        event = db.execute("SELECT * FROM events WHERE id=?;",
                           (event_id,))[0]  # Pass event_id as a tuple
    except:
        return render_template("404.html")

    return render_template(
        "event_details.html", event=event
    )
