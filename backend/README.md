## Installation

make a python3.9 virtual env

```
pip install -r requirements.txt
```

## useful management commands

In order to do most things you will need to run the development database.
In a separate terminal:

```
cd ../database/localhost
docker-compose up
```

Now you can do the following:

- `python manage.py migrate` this creates all the database models
- `python manage.py test` run the tests
- `python manage.py shell` this drops into a python shell. You can now interact with the database via the various models.
- `python manage.py runserver` launch the development server

## Interacting with the Django guis

Note that if the database isn't running or the tables haven't been set up yet, this isn't going to work!

To create a superuser:

```
python manage.py createsuperuser
```
The superuser can log into the admin panel and browse the apis frontend.

Now if you run the development server (`python manage.py runserver`), you'll be able to log in with your superuser and poke around:

- http://127.0.0.1:8000/admin
- http://127.0.0.1:8000/api

##  creating data to play with

You can create some curriculums in the database like this:

```
python manage.py import_curriculum dev_helpers/data/intro-to-tilde-course.json
python manage.py import_curriculum dev_helpers/data/data-eng-part-1.json
```

You will now be able to see the curriculums in the django gui: http://127.0.0.1:8000/admin/core/curriculum/

They will also be available in the api.

There are a few other management commands that can make dev-life a bit more convenient.

If a command's name is `command_name` then you can access it's documentation by typing in:

```
python manage.py command_name --help
```

### Creating users and teams

- `create_full_user`. Example usage: `python manage.py create_full_user someone.nice@example.com 1 1  first last umuzibot`
- `set_password`. Example usage:  `python manage.py set_password someone.nice@example.com  --password=supersecret`
- `create_team`. Example usage: `python manage.py create_team "demo team"`
- `add_users_to_team` Example usage: `python manage.py add_users_to_team  "someone.nice@example.com"  "demo team"`

### Curriculums and cards

- `import_curriculum` Example usage: `python manage.py import_curriculum dev_helpers/data/intro-to-tilde-course.json`
- `add_course_reg` Example usage:: `python manage.py add_course_reg "someone.nice@example.com" "Intro to Tilde for tech bootcamps" 0`
- `delete_and_recreate_user_cards` Example usage: `python manage.py delete_and_recreate_user_cards someone.nice@example.com`

### you can also give people permissions over different things

- `add_team_permission` Example usage: `python manage.py add_team_permission someone.nice@example.com VIEW_ALL "demo team"`
- `remove_team_permission` Example usage: `python manage.py remove_team_permission someone.nice@example.com VIEW_ALL "demo team"`

You can see all the team permissions here: `core/models.py`. L:ook at the metaclass inside the `Team` model.

## Getting a picture of the model relationships

There are a lot of tables here. And a picture is worth a thousand words.

First some setup:

```
sudo apt install graphvis graphvis-dev
pip install -r dev_requirements.txt
```

```
mkdir gitignore
python manage.py graph_models -a -g -o gitignore/all_models.png

# or you can draw the models for a specific app

python manage.py graph_models -g -o gitignore/core_models.png core
python manage.py graph_models -g -o gitignore/curriculum_tracking_models.png curriculum_tracking
python manage.py graph_models -g -o gitignore/git_real_models.png git_real
python manage.py graph_models -g -o gitignore/social_auth_models.png social_auth
```

You can also see how multiple apps relate to one another:
```
python manage.py graph_models -g -o gitignore/core_and_curriculum_tracking_models.png curriculum_tracking core
```

## Interacting with Github

If you aren't making use of the Tilde functionality involved in creating and managing repos, then you dont need to worry about this.

When a user on the Tilde frontend hits "start project" for any repo project, then the backend needs to interact with github as a specific user. The default here is a user names `umuzibot`.

I'm not going to give you `umuzibot`'s github login details. You are going to need to set up your own github profile.

The github profile that you have created will need to be able to create repos and set up branch protection rules and that sort of thing.

Make use of the following environmental variables to change that stuff:

```
export GITHUB_CLIENT_ID=??? Needed for login with github to work
export GITHUB_CLIENT_SECRET=??? Needed for login with github to
export GIT_REAL_ORG="the name of the organisation as registered on Github.com"
export GIT_REAL_BOT_USERNAME="the name of the user that will be sending out repo invites and that sort of thing"
```

Then create a user on Tilde through the management scripts. Give the user your GIT_REAL_BOT_USERNAME as the github username.

Now run the development server and do some logging in to make sure Tilde can do it's thing:

```
python manage.py runserver
```

- visit: http://localhost:8000/admin
- Login
- visit: http://localhost:8000/social_auth/github_oauth_start

## Environmental variables

There are a few environmental vars that are very hella useful in a development environment. Since you are using a virtualenv, I suggest you export them in your activate script.

If your system is set up the same as mine you would edit `~/.Virtualenvs/tilde3.9/bin/activate`. But you might keep your venvs somewhere else.

```
export REACT_APP_GOOGLE_CLIENT_ID=??? # used for the login with google function on the frontend
export GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE=??? # needed for login with google

export REACT_APP_FEATURE_AUTHENTICATION=1 # todo: check if we still use this
export REACT_APP_FEATURE_BACKEND_API_ON=1 # todo: check if we still use this

export GITHUB_CLIENT_ID=??? Needed for login with github to work
export GITHUB_CLIENT_SECRET=??? Needed for login with github to
```
