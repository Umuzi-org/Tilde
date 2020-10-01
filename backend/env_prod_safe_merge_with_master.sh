#!/bin/sh 

git checkout master 
git pull
git checkout env/prod 
git pull

cp -r core/migrations core/prod_migrations
cp -r attendance/migrations attendance/prod_migrations
cp -r curriculum_tracking/migrations curriculum_tracking/prod_migrations
cp -r git_real/migrations git_real/prod_migrations
cp -r social_auth/migrations social_auth/prod_migrations

git merge master

rm -rf core/migrations
rm -rf attendance/migrations
rm -rf curriculum_tracking/migrations
rm -rf git_real/migrations
rm -rf social_auth/migrations


cp -r core/prod_migrations core/migrations
cp -r attendance/prod_migrations attendance/migrations
cp -r curriculum_tracking/prod_migrations curriculum_tracking/migrations
cp -r git_real/prod_migrations git_real/migrations
cp -r social_auth/prod_migrations social_auth/migrations


python mange.py make_migrations




# git add -f core/migrations/*.py
# git add -f attendance/migrations/*.py
# git add -f curriculum_tracking/migrations/*.py
# git add -f git_real/migrations/*.py
# git add -f social_auth/migrations/*.py