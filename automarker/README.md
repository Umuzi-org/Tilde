# Automarker

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

In order to review code, the automarker will need to clone that code. It expects keys to be set up correctly, when cloning a private repo you will not be given the chance to input your github email and password or anything like that.

To review code, make a json POST request to the review-code endpoint. For example:

```
curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"repoUrl":"git@github.com:Umuzi-org/something.git","contentItemId":123, "flavours": ["python", "pytest"]}' \
http://localhost:1313/review-code

```
