from flask import Blueprint, session, request, render_template, flash, redirect
from database import db

movies_router = Blueprint(
    "movies_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@movies_router.route("/movies")
def list_movies(page_number=1, page_size=20):
    page_number = int(request.args.get("page_number", 1))
    page_size = int(request.args.get("page_size", 20))
    offset = (page_number - 1) * page_size
    result = db.execute(
        "SELECT * FROM movies ORDER BY release DESC LIMIT ? OFFSET ?;",
        page_size,
        offset,
    )
    return render_template("movies.html", movies=result)


@movies_router.route("/movies/<movie_id>")
def movie_details(movie_id):
    try:
        movie = db.execute("SELECT * FROM movies WHERE id=?;", movie_id)[0]
    except:
        return render_template("404.html")
    actors = db.execute(
        "SELECT name, photo FROM people JOIN movies_actors ON movies_actors.people_id = people.id WHERE movie_id = ?;",
        movie_id,
    )
    directors = db.execute(
        "SELECT name, photo FROM people JOIN movies_directors ON movies_directors.people_id = people.id WHERE movie_id = ?;",
        movie_id,
    )
    return render_template(
        "movie_details.html", movie=movie, actors=actors, directors=directors
    )
