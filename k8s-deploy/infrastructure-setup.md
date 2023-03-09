# Infrastructure setup

These notes document the process of setting up the staging environment. At some point it would be useful to translate this into some kind of infrastructure as code setup, eg using https://www.pulumi.com/. For now we are doing things by hand.

## Step 1: Create google project 

Pretty straight-forward. 

## Step 2: Database

### 2.1 Server 

https://console.cloud.google.com/sql/instances/create;engine=PostgreSQL?project=umuzi-staging 

Currently our prod db is using postgres9.6 so use that. We'll need to upgrade it at some point. 

Manually copied settings from prod: 
- vCPU
- RAM
- HDD/SSD size

Turned off backups and protections

### 2.2 User and database 

Open up a google cloud shell instance and do this:

```
CREATE DATABASE tilde_staging;
CREATE USER yyyyy WITH PASSWORD 'xxxxx';
GRANT ALL PRIVILEGES ON DATABASE "tilde_staging" to yyyyy;
```

## 2.3: Connect via local proxy to run migrations

Create a service account: 

https://console.cloud.google.com/iam-admin/serviceaccounts?project=umuzi-staging

Give it sql permissions that match those in prod. 

TODO: check that permissions are not excessive 

Download a json key.

Set the following environmental variables:

```
export SQL_CONNECTION_NAME="umuzi-staging:europe-west2:staging"


export TILDE_SQL_PORT="5437"
export TILDE_SQL_USER="???"
export TILDE_SQL_DB="???"
export TILDE_SQL_PASS="???"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

Now you should be able to run the proxy and migrations in the usual way.

Make use of python manage.py create_demo_data to populate the database with some fake users to play with.

## Step 3: Cluster setup  

https://console.cloud.google.com/kubernetes/list/overview?orgonly=true&project=umuzi-staging&supportedpurview=organizationId

Choose to create a new cluster. 
Select "Standard", not autopilot 
Select the version that most closely matches that in prod. 

Note: prod is currently using version 1.23.14-gke.1800. This is no longer available at time of writing. 




## Step 4: deploy staging

source your secrets then:

```
gcloud container clusters get-credentials tillde-cluster-staging  --zone europe-west2-a --project umuzi-staging

./upload-secrets.sh
```


Use this script whenever you want to deploy a version to staging.

```
./deploy-staging.sh 
```

TODO: add deploy static stuffs. 


## Reserve static ip 


## Step : SSL cert 

## Rabbit MQ

TODO

## Step : frontend 

This actually requires no setup. Just deploy the frontend code using the deploy script inside the frontend directory of this repo.