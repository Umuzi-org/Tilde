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
- `python manage.py shell` this drops into a python shell. You can now interact with the database via the various models.
- `python manage.py runserver` launch the development server
- `python manage.py test` run the tests

## setting up some test data

TODO
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
# EVERYTHING BELOW THIS LINE NEEDS TLC

## Environmental variables

You need the following configuration to be available in your environment

```
export GIT_REAL_CLONE_DIR=$HOME/.git_real_sync # we need to clone some repos during etl. Where sahould they go
export GIT_REAL_PERSONAL_GITHUB_NAME=[YOUR GITHUB USER]
export GITHUB_CLIENT_ID=[OAUTH_CREDS]
export GITHUB_CLIENT_SECRET=[OAUTH_CREDS]
export GOOGLE_SHEETS_CREDENTIALS_FILE=[PATH_TO_G_SHEETS_CREDS]

# and this one is for loading the curriculum into the database
export CURRICULUM_CLONE_DIR=$HOME/.curriculum_sync
```

## Running all the ETLs

1. create a superuser. Use your real umuzi email address because otherwise the etl might result in contradictory data
2. Load up the users and their github names: `python manage.py users_etl`
   If you forgot to make your user you might need to set it up via `python manage.py shell`

```
from core.models import User
u = User.objects.get(email="your.name@umuzi.org")
u.is_superuser = True
u.is_staff = True
u.set_password("your password")
u.save()
```

3. Log into github via the admin portal

```
python manage.py runserver
```

- visit: http://localhost:8000/admin
- Login
- http://localhost:8000/social_auth/github_oauth_start

4. Prune the noobs who can't follow simple instructions and should be shamed with a bell `python manage.py git_real_prune_broken_github_names`

### Github stuff

Once repos are pulled then you can do the rest in any order

```
python manage.py git_real_pull_repos
python manage.py git_real_pull_commits
python manage.py git_real_pull_prs
```
