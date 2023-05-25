# Cloud SQL Proxy

When this application is live (ie: deployed on the cloud) then it is backed by a Google Cloud SQL instance. You will need to interact with the Cloud SQL if:

- you want to query the database
- you want to make migrations or run migrations

You should not be using this database for day to day development activity.

## How it works

Basically, talking directly to the cloudsql database from your localhost isn't that straight forward. All communications need to go through a proxy. The information flows like this:

localhost <--> SQL cloud Proxy <---> CloudSQL

To start the proxy, do the following:

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service/account/key.json"
export SQL_CONNECTION_NAME="The google cloud connection name"
./start_sql_cloud_proxy.sh   # start the proxy
```

Now if you want to connect to your sql cloud instance from your django app you need to feed your app the correct sql settings. Something like this:

```
export SQL_DB=""
export SQL_USER=""
export SQL_PASS=""

# GOOD :D

python manage.py makemigrations
python manage.py migrate

# BAD T_T

python manage.py test
```
