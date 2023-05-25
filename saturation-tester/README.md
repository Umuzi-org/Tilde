# Saturation testing

The tilde mini frontend needs to be able to handle around 10000 users in a day. That's quite a lot.

We have a few different things that need to be tested out. Initially, each of these will be tested individually. 

- the mini frontend itself - initially we'll just `GET` the home page.
- the backend apis - users need to be able to start and finish steps, as well as submit code for review 
- the automarker - in prod we wont be able to access this directly, but on the staging environment we'll be able to access it via an ip address 
- rabbitmq - this is the connection between the api and the automarker. We'll need to make sure that if a lot of users submit things for review then nothing will fall over

## Locust 

- Read the docs here: https://docs.locust.io/en/stable/what-is-locust.html
- See the basics on how to run tests and interpret results here: https://docs.locust.io/en/stable/quickstart.html

## to install 

```
pipenv install
```

## To run

Activate the virtualenv and then use the `locust` command.

```
pipenv shell

source staging_urls.sh // you could also use localhost if you want to 
locust -f src/locustfile-mini-frontend.py // replace with whichever locustfile you want
```

## Plan of action 

This is still a bit of an experiment. Here's the plan:

1. Write the basic tests and increase the total user count until the total requests per second graph levels out. This means that the service is saturated
2. If the number of users is too low then tweak the infrastructure until we can handle the required number of simultanious users
3. Note what changes were needed. Was it an increase in ram? cpu? Number of pods? 

Ideally we should be able to very easily see which levers to pull on if we want to handle any number of users. 

