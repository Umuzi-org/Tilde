#!/bin/sh

while true
do
python manage.py mark_files_and_peer_reviews 0
sleep 1800  # half an hour
done
