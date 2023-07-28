# Movies and Shows Project for students

##### The aim of this project is just to teach the students some fundamental concepts and optimization was **NOT** considered at all.

To run this project, most importantly, python needs to be installed on the host machine. To check if python is installed, run
`python --version`
OR
`py --version`. If it returns a version number, then you're good to go. If it throws an error like '_Command is not recognized or Found_' then you should install python first.

Also, you need to have sqlite3 installed to. To check that, run: `sqlite3 --version`. If it is not installed, go ahead and install it.

Now that we have python installed, follow the steps:

- Open a terminal and `cd` into the folder of the project.
- Run `python -m venv venv` and wait a few seconds until it finishes.
- Depending on your OS:

  - Windows: Run `./venv/Scripts/activate`
  - Mac or Linux: Run `./venv/bin/activate`

- Run `pip install -r requirements.txt` and wait until it finishes installing the packages required.
- Now in the terminal, run: `python app.py` and it will start the server, now you can visit these routes:

| Route                            | Html to Render                            |
| -------------------------------- | ----------------------------------------- |
| `/`                              | `templates/index.html`                    |
| `/movies`                        | `templates/movies.html`                   |
| `/movies/<movie_id>`             | `templates/movie_details.html`            |
| `/admin/movies`                  | `templates/admin/movies/movies_list.html` |
| `/admin/movies/add`              | `templates/admin/movies/movie_add.html`   |
| `/admin/movies/<movie_id>/edit`  | `templates/admin/movies/movie_edit.html`  |
| `/admin/people`                  | `templates/admin/people/people_list.html` |
| `/admin/people/add`              | `templates/admin/people/people_add.html`  |
| `/admin/people/<people_id>/edit` | `templates/admin/people/people_edit.html` |
