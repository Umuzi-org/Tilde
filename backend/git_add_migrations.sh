#!/bin/sh 

python manage.py makemigrations attendance
python manage.py makemigrations core
python manage.py makemigrations curriculum_tracking
python manage.py makemigrations git_real
python manage.py makemigrations social_auth

python manage.py migrate attendance
python manage.py migrate core
python manage.py migrate curriculum_tracking
python manage.py migrate git_real
python manage.py migrate social_auth


git add -f attendance/migrations/*.py
git add -f core/migrations/*.py
git add -f curriculum_tracking/migrations/*.py
git add -f git_real/migrations/*.py
git add -f social_auth/migrations/*.py


rm attendance/migrations/*.py
rm core/migrations/*.py
rm curriculum_tracking/migrations/*.py
rm git_real/migrations/*.py
rm social_auth/migrations/*.py



rm -r attendance/migrations
rm -r core/migrations
rm -r curriculum_tracking/migrations
rm -r git_real/migrations
rm -r social_auth/migrations


cp -r ../../tilde-temp/backend/attendance/migrations attendance/
cp -r ../../tilde-temp/backend/core/migrations core/
cp -r ../../tilde-temp/backend/curriculum_tracking/migrations curriculum_tracking/
cp -r ../../tilde-temp/backend/git_real/migrations git_real/
cp -r ../../tilde-temp/backend/social_auth/migrations social_auth/