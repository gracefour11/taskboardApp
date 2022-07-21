# CS50W Capstone: Taskboard
This is a Taskboard app inspired by Google TasksBoard. Users can create their own taskboards and share them with other members of the app. They can create, manage and assign tasks on a full-screen Kanban board.

## Distinctiveness and Complexity
I consider that this project meets all the expectations raised in the assignment of the CS50W final project, as it is a web platform that implements most of the concepts and techniques taught in the course.

The project was built using Django as a backend framework and JavaScript as a frontend programming language. All generated information are saved in database (SQLite by default).

All webpages of the project are mobile-responsive. I have included the Material Bootstrap library to make my front-end components mobile-responsive.

The difference between this web app and previous projects is that this application makes use and manages the data to create/read/update/delete taskboards and tasks instantly. Taskboards can be modified without reloading the page.

## Installation
  - Install project dependencies by running `pip install -r requirements.txt`. 
  - Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
  - Create superuser with `python manage.py createsuperuser`. This step is optional.
  - Run `python manage.py runserver` to start the app.
  - Go to website address and register an account.

## Structure
  - `taskboard` - main application directory.
    - `static/taskboard` contains all static content.
        - `css` contains all the CSS files.
        - `js` contains all JavaScript files used in project.
            - `index.js` - script that run in `index.html` template.
            - `taskboard.js` - script that run in `taskboard.html` template.
        - `media` contains all images used in project.
    - `templates/taskboard` contains all application templates.
        - `layout.html` - base templates. All other templates extend it.
        - `welcome.html` - main template for unregistered users. It shows login and registration forms.
        - `index.html` - main templates that shows all the taskboards (only for registered users).
        - `taskboard.html` - template that shows a taskboard page.

    - `models.py` contains the models I used in the project: 
        1. `User` model extends the standard AbstractUser model.
        2. `Taskboard` model is for taskboards.
        3. `User2Taskboard` represents the mapping of users to taskboards.
        4. `Task` model is for tasks.
        
    - `urls.py` - all application URLs.
    - `views.py` respectively, contains all application views.
  - `capstone` - project directory.
