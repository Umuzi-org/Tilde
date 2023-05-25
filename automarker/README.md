# Auto-marker

When a learner moves through one of our courses they do a bunch of projects. Many of the projects are or can be specced in a way that makes the learner code very predictable. They are asked to create files with specific names in specific places. They are also asked to create classes and functions with specific names and functionality.

Reviewing that code is very boring and repetitive. The automarker exists to reduce that workload.

When it comes to code projects, the automarker basically does the following:

1. It clones the learner's repo
2. If the learner was tasked with writing thests, then the automarker checks if those tests pass (it doesn't currently check if those tests are thorough, but it's a start)
3. It then runs a set of standard tests against the learner's code

## Architecture

This is a lil express app with a few endpoints. Since the Tilde repo is public and plagiarism is lame, we store the automarker configuration in a separate repo. That repo contains a bunch of "perfect" projects that line up with our syllabus.

## get it to run on your computer

This is an express app. To get it up and running:

```
npm install

# set up your environmental variables:
## VERY IMPORTANT

# The automarker needs to know where the configuration repo lives. Use an
# environmental variable to get that to work:

export AUTO_MARKER_CONFIGURATION_REPO_PATH=/path/to/acn-automarker-config

# take a look at env.mjs to see the other environmental variables

# next up. start the server:

npm run start:dev

# To check if it is alive:

curl http://localhost:1337/health-check
```

## Configuration

If you add/edit any configuration in the config repo, then you'll want to test it out before runnin it against ny learner code.

### Testing the configuration

Every project that we want to automark is configured in a separate repo. That repo contains a perfect version of the project.

Use the test-config endpoint to make sure that the test configuration works. That includes actually running the automarker against the perfect project.

When introducing new configuration to the configuration repo, it's important to run this self-check!

Eg api call:

```
# javascript

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":273, "flavours": ["javascript"]}' \
http://localhost:1337/test-config

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":223, "flavours": ["javascript"]}' \
http://localhost:1337/test-config

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":756, "flavours": ["javascript"]}' \
http://localhost:1337/test-config

#  python

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":273, "flavours": ["python"]}' \
http://localhost:1337/test-config

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":223, "flavours": ["python"]}' \
http://localhost:1337/test-config

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":756, "flavours": ["python"]}' \
http://localhost:1337/test-config

# java

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":273, "flavours": ["java"]}' \
http://localhost:1337/test-config

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":223, "flavours": ["java"]}' \
http://localhost:1337/test-config

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":756, "flavours": ["java"]}' \
http://localhost:1337/test-config

```

### The mark project endpoint

To review actual learner code, make a json POST request to the mark-project endpoint.

Here are a few examples of passing code:

```
curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-python.git","contentItemId":273, "flavours": ["pytest","python"]}' \
http://localhost:1337/mark-project

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-python.git","contentItemId":273, "flavours": ["pytest","python"]}' \
http://localhost:1337/mark-project

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-js.git","contentItemId":273, "flavours": ["javascript"]}' \
http://localhost:1337/mark-project

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-simple-calculator-java.git","contentItemId":273, "flavours": ["java"]}' \
http://localhost:1337/mark-project

curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/perfect-person-java.git","contentItemId":223, "flavours": ["java"]}' \
http://localhost:1337/mark-project

```

- The repo url format needs to be: `git@github.com:{things}.git` (so your github keys should be set up)
- The content item id should be a number
- The flavours should exactly match the project you are reviewing. The order doesn't matter.

## Security

Ok...so this is a bit sketchy. Please note that if you clone a project to mark, that project can execute arbitrary code on your computer. Ok, it's very sketchy.

This is sortof ok because you should really only be using this to review code that is in the review column on Tilde. So if people do sketchy things then we know where they live

When running this application in a production environment then the automarker will be in a docker container that is isolated through use of a cloud service provider's own isolation mechanisms. Executing arbitrary code within the container is still dangerous in that github keys can be stolen. Github keys will be the only sensitive piece of information known to the image.

### How will we overcome this?

Probably by having multiple containers with a shared volume.

Container 1 will only be in charge of cloning repos. It will need a github key to do this.

Container 2 will have access to the clone destination and nothing else. It will be in charge of actually running the tests.

Static analysis can also be helpful on certain projects. Eg for certain projects there should be no import/require statements.

## Future work

Right now things are set up so we can check if a submitted project passes a given set of tests. But we don't check to see if a submitted suite of tests is sufficient.

It could be useful to run the learner's tests against code with known problems.

We could do this by creating a bunch of imperfect projects. We would expect the learner's tests to fail when run against the imperfect projects.
