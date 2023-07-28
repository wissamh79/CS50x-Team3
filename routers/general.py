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
    featured_movies = db.execute("SELECT * FROM movies WHERE is_featured = True;")
    featured_shows = db.execute("SELECT * FROM shows WHERE is_featured = True;")
    movies = db.execute("SELECT * FROM movies ORDER BY release DESC LIMIT 10;")
    shows = db.execute("SELECT * FROM shows ORDER BY release DESC LIMIT 10;")
    data = {
        "featured_movies": featured_movies,
        "featured_shows": featured_shows,
        "movies": movies,
        "shows": shows,
    }
    return render_template("index.html", data=data)
