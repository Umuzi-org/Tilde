# Quick start

This guide will help you get set up to run all these goodies locally.

Here's a video that shows you all the things: https://www.youtube.com/watch?v=NXpwv5CO5Dg&feature=youtu.be

## Prerequisites

We use docker-compose and Python3.9

- [Docker](https://www.docker.com/) and Docker Compose - to run the DB for the backend. If you install Docker Desktop, you get Docker Compose, but if you install with your CLI such as on Linux then you need to install Docker Compose separately after installing Docker.
- [Python](https://www.python.org/) 3.9+ - to run the backend.
- [Node.js](https://nodejs.org/en/) - to run the frontend.

## Database server

This project uses a Postgres database in a container.

You can get a local test and development database up and running by doing the following:

```sh
cd database/localhost
docker-compose up
```

You'll notice that it creates a folder called gitignore (we've told git to ignore all directories named gitignore). That's where the data is stored. So if you ever want to completely start over with the database then you can just kill the composition and delete that directory.

When you `docker-compose up` again, your DB will be fresh as a daisy.

## Backend

The backend is written in Django. We're going to start the Django app with the commands below.

Make sure the DB is up first, then continue.

```sh
cd backend

# create a virtual environment
python3 -m venv venv

# please make sure you never commit your virtualenv directory to git!
# if you prefer to use virtualenvwrapper then that would be totally fine

# activate it
source venv/bin/activate

# install dependencies
pip install wheel
pip install -r requirements.txt
playwright install
```

Make sure it works by running the tests:

```sh
python manage.py test --failfast
```

The `failfast` flag isn't strictly necessary, but it does speed things up.

Once that is done you'll be able to activate your virtual environment at any time and execute application commands.

The first thing you'll want to do now is get Django to create tables in your database.

```sh
python manage.py migrate
```

Then you might want to create a superuser for yourself:

```sh
python manage.py createsuperuser
```

Or perhaps create some demo users:

```sh 
python manage.py create_demo_data
```

To see what the above command does, take a look [here](backend/curriculum_tracking/management/commands/create_demo_data.py). Look for `def handle` in the code to see what is happening.


To run the development server:

```sh
python manage.py runserver
```

The admin panel is available at `/admin`.
The browsable is available at `/api`.


## Frontend

This is a standard React application. For it to function correctly, the backend needs to be up and running.

```sh
cd frontend
npm install
npm start
```

That's it. By default, it will connect to the Django app you just launched.

We make use of [storybook](https://storybook.js.org/). You can launch that with: 

```
npm run storybook
```

### Running the tests

1. `npm test`

That's it.

Please notes, the frontend tests are in no way sufficient. We were kinda in a hurry and still need to make some decisions about testing standards.

## Getting login with Google to work

Users can either login with an email and password, or using Google. You don't need login with Google to work if you want to use the application.

Follow this tutorial to get some credentials:

https://developers.google.com/identity/sign-in/web/sign-in

Once you have your credentials file then you need to make sure that your environmental variables are set up.

You need this available in your frontend in order to get the login to work:

```sh
export REACT_APP_GOOGLE_CLIENT_ID="the client id in the secrets file"
```

And then the backend needs this:

```sh
export GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE=/path/to/your/credentials/file
```

A nice way to set up your environmental variables is to export all the things at the top of your virtualenvironment activate script. Then whenever you run the frontend or the backend, activate the same venv. This is nice because then the whole lot is specified in one place and if you need to change your keys or anything then it's easy peasy.

## Creating a user and their cards

There are a few convenience commands that you can use to set things up for first time use/poking around:

Note, to see details of any of these commands you can do the following: `python manage.py THE_COMMAND --help`

```sh
# create your sweet self as a superuser
python manage.py create_full_user example@email.com true true sheenarbw
python manage.py set_password example@email.com example@email.com

# add a new group
python manage.py create_team "demo team"

# add a user to a group with default permissions. You can use this command to set people up with different roles

python manage.py add_user_to_team "example@email.com" "demo team"


# add a curriculum. This sets up a simple course that demonstrates all card features
# generally curriculums are not created like this, usually they are stored as markdown files in a seperate repo

python manage.py import_curriculum dev_helpers/data/intro-to-tilde-course.json

# register a user for a course
# the intro to Tilde course basically demonstrates all the different things Tilde can do from a student's perspective so it's a good way to get to poke around with all functionality
python manage.py add_course_reg "example@email.com" "Tilde: Intro for students"

# regenerate cards for the user
python manage.py delete_and_recreate_user_cards "example@email.com"
```

If you follow these steps, then you should be able to log into the frontend as this user and poke around your board.
