# Quick start

This guide will help you get set up to run all these goodies locally.

## Prerequisites

We use docker-compose and Python3. That's about it.

## Database server

We are running Postgres. You can get a local test and development database up and running by doing the following:

```
cd database/localhost
docker-compose up
```

You'll notice that it creates a folder called gitignore (we've told git to ignore all folders named gitignore). That's where the data is stored. So if you ever want to completely start over with the database then you can just kill the composition and delete that directory.

When you `docker-compose up` again your db will be fresh as a daisy.

## Backend

The backend is written in Django. For this to be up and running the database needs to be up and running.

To set it up you need to be running Python 3. Seriously, this wont work with Python2 at all.

```
cd backend

# make yourself a virtualenv
python3 -m venv venv

# please make sure you never commit your virtualenv directory to git!

# activate it
source venv/activate

# install dependencies
pip install wheel
pip install -r requirements.txt
```

Make sure it works by running the tests:

```
python manage.py test
```

Once that is done you'll be able to activate your virtual environment at any time and execute application commands.

The first thing you'll want to do now is get Django to create tables in your database.

```
python manage.py migrate
```

Then you might want to create a superuser for yourself:

```
python manage.py createsuperuser
```

And lastly you will want to be able to run the development server:

```
python manage.py runserver
```

The admin panel is available at `/admin`, and the

### Running the tests

1. make sure that the database is up and running
2. activate your virtualenv
3. `python manage.py test`

## Frontend

This is a perfectly normal React application. For it to function correctly, the backend needs to be up and running.

```
cd frontend
npm install
npm start
```

That's it. By default it will connect to the django app you just launched.

### Running the tests

1. `npm test`

That's it.

Please notes, the frontend tests are in now way sufficient. We were kinda in a hurry and still need to make some decisions about testing standards.

## Getting login with Google to work

This is only needed if you want to run the frontend and actually use it. Unfortunately our only login mechanism is Google so that's a bit of a pain in the neck. The first thing you need to do is get some credentials.

Usually this tutorial is the way to go.
https://developers.google.com/identity/sign-in/web/sign-in

If you are devving on your localhost, we have some credentials you can use. Come say hi on our discord server and we'll share.

Once you have your credentials file then you need to make sure that your environmental variables are set up.

You need this available in your frontend in order to get the login to work:

```
export REACT_APP_GOOGLE_CLIENT_ID="the client id in the secrets file"
```

And then the backend needs this:

```
export GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE=/path/to/your/credentials/file
```

What I generally do is export all the things at the top of by virtualenvironment activate script. Then whenever I run the frontend or the backend I activate the same venv. This is nice because then the whole lot is specified in one place and if you need to change your keys or anything then it's easy peasy.
