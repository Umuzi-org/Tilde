# Auto-marker

One cool thing about having a standard set of fundamental projects is that we can have a standard set of tests to check if they work properly.

The automarker basically clones a learners git repo and checks if it works. It returns a message.

## get it to run on your computer

This is an express app. To get it up and running:

```
npm install

# set up your environmental variables:
# eg you can set the PORT like this

export AUTO_MARKER_PORT=1313

# take a look at env.mjs to see the other environmental variables

# next up. start the server:

npm run start:dev

# To check if it is alive:

curl http://localhost:1313/health-check
```

## reviewing code

### The setup

In order to review code, you will need to have cloned the automarker configuration repo and put it somewhere sensible. Set `CONFIGURATION_REPO_PATH` to point to the configuration repo.

The auto-marker will need to clone that code you are marking. It expects keys to be set up correctly, when cloning a private repo you will not be given the chance to input your github email and password or anything like that.

### The mark project endpoint

To review code, make a json POST request to the mark-project endpoint. For example:

```
curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-python.git","contentItemId":273, "flavours": ["pytest","python"]}' \
http://localhost:1313/mark-project


curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-js.git","contentItemId":273, "flavours": ["javascript"]}' \
http://localhost:1313/mark-project



curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-java.git","contentItemId":273, "flavours": ["java"]}' \
http://localhost:1313/mark-project



curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-person-java.git","contentItemId":223, "flavours": ["java"]}' \
http://localhost:1313/mark-project


```

- The repo url format needs to be: `git@github.com:{things}.git`
- The content item id should be a number
- The flavours should exactly match the project you are reviewing. The order doesn't matter.

## Security

Ok...so this is a bit sketchy. Please note that if you clone a project to mark, that project can execute arbitrary code on your computer.

This is sortof ok because you should really only be using this to review code that is in the review column on Tilde. That means that PRs have been seen, reviewed and merged by people who are allocated as reviewers.

That said, this is still a bit sketchy.

When running this application in a production environment then the automarker will be in a docker container that is isolated through use of a cloud service provider's own isolation mechanisms. Executing arbitrary code within the container is still dangerous in that github keys can be stolen. Github keys will be the only sensitive piece of information known to the image.

### How will we overcome this?

Probably by having multiple containers with a shared volume.

Container 1 will only be in charge of cloning repos. It will need a github key to do this.

Container 2 will have access to the clone destination and nothing else. It will be in charge of actually running the tests.

## Future work

The production url is: https://automark-sdn7qm5gxa-ew.a.run.app

curl https://automark-sdn7qm5gxa-ew.a.run.app/healthcheck

https://automark-sdn7qm5gxa-ew.a.run.app/mark-project
