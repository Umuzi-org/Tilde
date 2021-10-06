# Quick start

This guide will help you get set up to run all these goodies locally.

Here's a video that shows you all the things: https://www.youtube.com/watch?v=NXpwv5CO5Dg&feature=youtu.be

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose - to run the DB for the backend. If you install Docker Desktop, you get Docker Compose, but if you install with your CLI such as on Linux then you need to install Docker Compose separately after installing Docker.
- [Python](https://www.python.org/) version 3 - to run the backend.
- [Node.js](https://nodejs.org/en/) - to run the frontend.

## Database server

This project uses a Postgres database in a container. 

You can get a local test and development database up and running by doing the following:

```sh
cd database/localhost
docker-compose up
```

You'll notice that it creates a folder called gitignore (we've told git to ignore all folders named gitignore). That's where the data is stored. So if you ever want to completely start over with the database then you can just kill the composition and delete that directory.

When you `docker-compose up` again, your DB will be fresh as a daisy.

## Backend

The backend is written in Django. We're going to start the Django app with the commands below.

Make sure the DB is up first before you continue.

```sh
cd backend

# create a virtual environment 
python3 -m venv venv

# please make sure you never commit your virtualenv directory to git!

# activate it
source venv/bin/activate

# install dependencies
pip install wheel
pip install -r requirements.txt
```

Make sure it works by running the tests:

```sh
python manage.py test
```

Once that is done you'll be able to activate your virtual environment at any time and execute application commands.

The first thing you'll want to do now is get Django to create tables in your database.

```sh
python manage.py migrate
```

Then you might want to create a superuser for yourself:

```sh
python manage.py createsuperuser
```

And lastly, to run the development server:

```sh
python manage.py runserver
```

The admin panel is available at `/admin`.

### Running the tests

1. Make sure that the database is up and running
2. ACtivate your virtualenv
3. Run tests.
    ```sh
    python manage.py test
    ```

## Frontend

This is a standard React application. For it to function correctly, the backend needs to be up and running.

```sh
cd frontend
npm install
npm start
```

That's it. By default, it will connect to the Django app you just launched.

### Running the tests

1. `npm test`

That's it.

Please notes, the frontend tests are in no way sufficient. We were kinda in a hurry and still need to make some decisions about testing standards.

## Getting login with Google to work

This is only needed if you want to run the frontend and actually use it. Unfortunately our only login mechanism is Google so that's a bit of a pain in the neck. The first thing you need to do is get some credentials.

Usually this tutorial is the way to go.

https://developers.google.com/identity/sign-in/web/sign-in

If you are devving on your localhost, we have some credentials you can use. Come say hi on our discord server and we'll share.

Once you have your credentials file then you need to make sure that your environmental variables are set up.

You need this available in your frontend in order to get the login to work:

```sh
export REACT_APP_GOOGLE_CLIENT_ID="the client id in the secrets file"
```

And then the backend needs this:

```sh
export GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE=/path/to/your/credentials/file
```

What I generally do is export all the things at the top of by virtualenvironment activate script. Then whenever I run the frontend or the backend I activate the same venv. This is nice because then the whole lot is specified in one place and if you need to change your keys or anything then it's easy peasy.

## Creating a user and their cards

There are a few convenience commands that you can use to set things up for first time use/poking around:

Note, to see details of any of these commands you can do the following: `python manage.py THE_COMMAND --help`

```sh
# create your sweet self as a superuser
python manage.py create_full_user sheena.oconnell@umuzi.org true true sheenarbw
python manage.py set_password sheena.oconnell@umuzi.org sheena.oconnell@umuzi.org

# add a new group
python manage.py create_team "demo team"

# add a user to a group with default permissions. You can use this command to set people up with different roles

python manage.py add_user_to_team "sheena.oconnell@umuzi.org" "demo team"


# add a curriculum. This sets up a simple course that demonstrates all card features
# generally curriculums are not created like this, usually they are stored as markdown files in a seperate repo

python manage.py import_curriculum dev_helpers/data/intro-to-tilde-course.json

# register a user for a course
# the intro to Tilde course basically demonstrates all the different things Tilde can do from a student's perspective so it's a good way to get to poke around with all functionality
python manage.py add_course_reg "sheena.oconnell@umuzi.org" "Tilde: Intro for students"

# regenerate cards for the user
python manage.py delete_and_recreate_user_cards "sheena.oconnell@umuzi.org"
```

If you follow these steps, then you should be able to log into the frontend as this user and poke around your board.
