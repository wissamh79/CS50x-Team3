from flask import Blueprint, session, request, render_template, flash, redirect
from database import db
import requests

admin_router = Blueprint(
    "admin_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@admin_router.route("/movies")
def admin_movies_list():
    movies = db.execute("SELECT * FROM movies;")
    return render_template("admin/movies/movies_list.html", movies=movies)


@admin_router.route("/movies/add", methods=["GET", "POST"])
def admin_movies():
    if request.method == "GET":
        people = db.execute("SELECT id, name FROM people ORDER BY name ASC;")
        genres = db.execute("SELECT id, name FROM genres ORDER BY name ASC;")

        return render_template(
            "admin/movies/movie_add.html", data={"people": people, "genres": genres}
        )
    else:
        title = request.form.get("title")
        description = request.form.get("description")
        release = request.form.get("release")
        length = request.form.get("length")
        rating = request.form.get("rating")
        trailer = request.form.get("trailer")
        is_featured = True if request.form.get("is_featured") == "on" else False
        image = request.files.get("poster", None)
        genres = request.form.getlist("genre")
        actors = request.form.getlist("actors")
        directors = request.form.getlist("directors")

        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
        else:
            image = ""
        # Insert movies table information
        movie_id = db.execute(
            """
                   INSERT INTO movies 
                   (title, description, release, length, 
                   rating, trailer, is_featured, poster)
                   """,
            title,
            description,
            release,
            length,
            rating,
            trailer,
            bool(is_featured),
            image,
        )
        # Insert genres
        db.execute(
            """
                   INSERT INTO movies_genres (movie_id, genre_id)
                   SELECT ? AS movieID ,genres.id
                   FROM genres WHERE genres.id IN (?);
                   """,
            movie_id,
            genres,
        )
        # Insert Actors
        db.execute(
            """
                   INSERT INTO movies_actors (movie_id, people_id)
                   SELECT ? AS movieID ,people.id
                   FROM people WHERE people.id IN (?);
                   """,
            movie_id,
            actors,
        )
        # Insert Directors
        db.execute(
            """
                   INSERT INTO movies_directors (movie_id, people_id)
                   SELECT ? AS movieID ,people.id
                   FROM people WHERE people.id IN (?);
                   """,
            movie_id,
            directors,
        )
        return redirect("/admin/movies")


@admin_router.route("/movies/<movie_id>/edit", methods=["GET", "POST"])
def admin_movies_edit(movie_id):
    if request.method == "GET":
        try:
            movie = db.execute("SELECT * FROM movies WHERE id=?;", movie_id)[0]
        except:
            return render_template("404.html")
        genres = db.execute(
            """SELECT genres.id AS id,genres.name AS name, 
            CASE WHEN movies_genres.movie_id IS NULL THEN 0 ELSE 1 END AS exist
            FROM genres LEFT JOIN movies_genres ON genres.id = movies_genres.genre_id
            AND movies_genres.movie_id = ?""",
            movie_id,
        )

        actors = db.execute(
            """SELECT people.id as id, people.name as name,
            CASE WHEN movies_actors.movie_id IS NULL THEN 0 ELSE 1 END AS exist
            FROM people LEFT JOIN movies_actors ON people.id = movies_actors.people_id
            AND movies_actors.movie_id = ?;""",
            movie_id,
        )

        directors = db.execute(
            """SELECT people.id as id, people.name as name,
            CASE WHEN movies_directors.movie_id IS NULL THEN 0 ELSE 1 END AS exist
            FROM people LEFT JOIN movies_directors ON people.id = movies_directors.people_id
            AND movies_directors.movie_id = ?;""",
            movie_id,
        )

        return render_template(
            "admin/movies/movie_edit.html",
            movie=movie,
            genres=genres,
            directors=directors,
            actors=actors,
        )

    # Post Method
    else:
        genres = request.form.getlist("genres")
        actors = request.form.getlist("actors")
        directors = request.form.getlist("directors")
        title = request.form.get("title")
        release = request.form.get("release")
        description = request.form.get("description")
        length = request.form.get("length")
        rating = request.form.get("rating")
        trailer = request.form.get("trailer")
        is_featured = True if request.form.get("is_featured") == "on" else False
        image = request.files.get("poster", None)

        # If changed image, Upload new image.
        if image:
            res = requests.post(
                "https://api.imgbb.com/1/upload",
                files={"image": image},
                params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
            )
            if res.ok:
                data = res.json()
                image = data["data"]["url"]
        else:
            image = db.execute("SELECT poster FROM movies WHERE id=?", movie_id)[0][
                "poster"
            ]
        # Start updating
        db.execute(
            """
                   UPDATE movies SET title = ?, description = ?, release = ? , length = ?, rating = ?, poster = ?, trailer = ?, is_featured = ? WHERE id = ?;
                   """,
            title,
            description,
            release,
            length,
            float(rating),
            image,
            trailer,
            bool(is_featured),
            movie_id,
        )
        db.execute(
            """
                   INSERT INTO movies_genres (movie_id, genre_id)
                   
                    SELECT ? AS movieID, genres.id AS GenreID
                    FROM genres WHERE genres.id IN (?)
                    AND genres.id NOT IN (
                    SELECT genre_id FROM movies_genres WHERE movie_id = ?);
                   """,
            movie_id,
            genres,
            movie_id,
        )

        db.execute(
            """
                   INSERT INTO movies_actors (movie_id, people_id)
                   
                    SELECT ? AS movieID, people.id AS peopleID
                    FROM people WHERE people.id IN (?)
                    AND people.id NOT IN (
                    SELECT people_id FROM movies_actors WHERE movie_id = ?);
                   """,
            movie_id,
            actors,
            movie_id,
        )
        db.execute(
            """
                   INSERT INTO movies_directors (movie_id, people_id)
                   
                    SELECT ? AS movieID, people.id AS peopleID
                    FROM people WHERE people.id IN (?)
                    AND people.id NOT IN (
                    SELECT people_id FROM movies_directors WHERE movie_id = ?);
                   """,
            movie_id,
            directors,
            movie_id,
        )
        return redirect("/admin/movies")


@admin_router.route("/people")
def admin_people_list():
    people = db.execute("SELECT * FROM people;")
    return render_template("admin/people/people_list.html", people=people)


@admin_router.route("/people/add", methods=["GET", "POST"])
def admin_people():
    if request.method == "GET":
        return render_template("admin/people/people_add.html")

    name = request.form.get("name", None)
    image = request.files.get("photo")
    print(request.files)

    if image:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
            print(image)

    try:
        db.execute("INSERT INTO people (name, photo) VALUES (?,?);", name, image)
    except Exception as e:
        print(f"An Error has been generated\n".upper() + e)
        return render_template("failure.html")
    return redirect("/admin/people")


@admin_router.route("/people/<people_id>/edit", methods=["GET", "POST"])
def admin_people_edit(people_id):
    try:
        person = db.execute("SELECT * FROM people WHERE id = ?;", people_id)[0]
    except:
        return render_template("failure.html")
    if request.method == "GET":
        return render_template("admin/people/people_edit.html", person=person)

    name = request.form.get("name")
    image = request.files.get("photo")

    if not image:
        try:
            image = db.execute("SELECT photo FROM people WHERE id = ?")[0]["photo"]
        except:
            return render_template("failure.html")
    else:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
    db.execute("UPDATE people SET name = ?, photo = ?", name, image)
    return redirect("/admin/people")
