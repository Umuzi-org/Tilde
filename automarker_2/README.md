# Automarker 2

This project is an improvement on the last version of the automarker. It is designed to overcome certain shortcomings in previous versions.

It is a web app but can also be used as a command-line utility. This READE focuses on the command-line usecase since that is how it will most often be used.

## Installation 

1. Install your dependencies

First, install python3.10 and poetry then:

```
poetry install

# then, because spacey wants to be special:
poetry shell

<!-- pip install -U spacy   -->
python -m spacy download en_core_web_sm
```

2. Make sure you have the configuration repo cloned somewhere sensible

**IMPORTANT**: The configuration repo is private. If you commit it to a public repo (such as the Tilde repo) then you are letting learners cheat on every project. Please make sure you clone the repo to somewhere outside of the Tilde repo directory.

If the above statement doesn't make sense then please stop here and ask for help.

```
cd /somewhere/sensible/
git clone git@github.com:Umuzi-org/automarker-2-config.git 
```

At this point, your configuration repo will be at `/somewhere/sensible/automarker-2-config`. Take note of that path, you will need it later on. 

3. Make sure your github ssh key is set up 

The automarker needs to clone private repos in an automated way so an ssh key is needed. 

## How to run the unit tests

Note that there currently isn't very high coverage on the unit tests. Contributions are welcome.

```
poetry shell
python manage.py test
```

## How to run the automarker

1. Activate up your shell and make sure all the required environmental variables exported

```
poetry shell 
export AUTOMARKER_2_CONFIG_DIR=/somewhere/sensible/automarker-2-config
```

**A cool trick:** If you don't want to have to remember to `export` your environmental variables all the time then do this:

```
poetry shell
which python
```

This will print out the path to the Python executable associated with the current virtual environment. Eg: `/home/yourname/.VirtualEnvs/automarker_2-nDA8r9UM/bin/python`.

Now open up the `activate` script in that same directory:

`code /home/yourname/.VirtualEnvs/automarker_2-nDA8r9UM/bin/activate`

Paste your `export` statements right at the top.

Every time you execute `poetry shell` then you are really just `source`ing your `activate` script.


2. Run the appropriate command

eg:

```
python manage.py check_project_configuration.py 186 javascript
```

The commands are detailed below:

### Automarker commands

There are scripts available for everything you might want to do:
#### Mark a learner's code

Running the following command does the following:

1. Clones the learner's repo. The repo will be inside a directory called "gitignore"
2. runs our tests on the repo
3. Prints out results 

```
python manage.py mark_learner_project.py URL CONTENT_ITEM_ID FLAVORS 

eg:

python mark_learner_project 186 git@github.com:Umuzi-org/blah-blah-186-consume-github-api-python.git python
```

Pay close attention to the format of the repo url: `git@github.com:{owner}/{repo_name}.git`.  If you use a different format then the clone command might not work.

**IMPORTANT NOTE** The project configuration might not be perfect yet. 

- it is best to look at the learner's code before marking it as competent, even if the automarker says it's competent
- the automarker will try to come up with comments that will make sense to the learner. Please read the review that the automarker comes up with. If you think it is good enough then you can copy-paste it into the Tilde frontend but ALWAYS make sure it makes sense before doing that
- if the automarker is saying something confusingly then please either:
    - tell someone so it can be fixed; or
    - make a PR that fixes the problem
- if the automarker is not testing the learner code thoroughly enough on a specific project then please either:
    - tell someone about it so it can be fixed; or
    - make a pr that fixes the problem


#### Print configuration summary

If you want to quickly see if something is configured then you can either dig through the configuration repo, or you can run this command:

```
python manage.py print_configuration.py
```

You'll see a list of all the configuration that exists. 

Each line of the output will have the following format:

```
{name}[{content_item_id}] {matching flavours} {status}
eg:
consume_github_api[186] [['javascript']] DEBUG
```

- name: This is just for convenience, it just needs to be human-readable
- content_item_id: this needs to EXACTLY MATCH the content item id in the database
- matching flavors: probably obvious...
- status: this can have a few different values, described below 

**A cool trick:** Use `grep` to quickly get the subset of the information you are interested in. Here are a few examples:

```
# list only the python config
python manage.py print_configuration.py | grep python 

# list only the config that is deactivated 
python manage.py print_configuration.py | grep DEACTIVATED 

# list only the config that has the word github in it's name
python manage.py print_configuration.py | grep github 

# you can also use multiple greps
# eg: list only the javascript configuration that is in DEBUG mode
python manage.py print_configuration.py | grep javascript | grep DEBUG 
```

You can combine that with `wc` to count the number of projects in different statuses. Eg:

```
# How many configurations are there in total ?
python manage.py print_configuration.py |  wc -l 

# How many python configurations are there?
python manage.py print_configuration.py | grep python | wc -l 

# How many python configurations are in debug mode?
python manage.py print_configuration.py | grep python | grep DEBUG | wc -l 

```

##### Understanding configuration statuses

- NOT_IMPLEMENTED: We still need to build this one out
- DEBUG: The configuration is alive and kicking, but we aren't yet 100% confident in its output. Staff are encouraged to make use of this configuration in order to build confidence over time 
- PRODUCTION: The configuration has been battle tested. We are confident that the output is correct
- DEACTIVATED: This configuration was in DEBUG or PRODUCTION mode and something went wrong so we had to turn it off

#### Configuration self-testing 

This runs the tests against the configured "perfect project". This is useful if you are configuring projects yourself or if you are changing how any part of the automarker works.

```
python manage.py check_project_configuration.py CONTENT_ITEM_ID FLAVORS

# eg:

python manage.py check_project_configuration.py 186 javascript
```
### Running a command with multiple flavors 

If you ever need to input multiple flavors for a command then do it like so:

```
python manage.py check_project_configuration.py 999 javascript karma
python mark_learner_project.py git@github.com:Umuzi-org/blah-blah-999-consume-github-api-python.git 999 javascript karma 
```

In other words, the flavours should be separated by spaces.

## Contributions are welcome and encouraged!

If you see a problem in some automarker configuration then please:

1. Fix it
2. Test it out with the check_project_configuration script
3. Test it out on a few learner projects if you can dig some up
4. Make a PR 

If you see some way to improve the actual automarker machine then please go ahead and do that! Here are a few things that will be welcome, I'm sure you can think of more:

- bug fixes
- unit tests
- documentation
- making the output look better
- anything else that will make this easier to use
- anything else that will make this easier to contribute to

## Previous automarker shortcomings to overcome 

The previous automarker version has a number of problems. We are working to overcome the following: 

1. unDRY project configuration [DONE]

If we write configuration for a single project in multiple languages, then the various test cases need to be rewritten in multiple languages. There is no way for data to be shared.

2. central configuration file [DONE]

The code and the config are separate. The configuration file is unwieldy and so people keep putting things in random places instead of grouping configs sensibly. Config should be colocated with the code

3. Only one level of failure [DONE]

We should allow multiple levels. Eg: if the learner's code doesn't run at all (meaning, they didn't run it at all) then we would want to give them a bad review. On the other hand, if there is just a little bug we should not be as harsh. 

4. Rigid configuration [DONE]

It would be useful to be able to tweak the steps in different marker pipelines. Right now the only way to do that is to create whole new markers.

5. Testing frameworks do weird things between different languages [DONE]

Logs and errors get swallowed in different ways. It's hard to be consistent about gathering info and sharing it with the user.

6. Error text is not user-friendly [DONE]

Due to the weird things that happen between languages, it is hard to give learners good quality feedback. 

7. No visibility of test runs [DONE in command-line commands, still needs work in live environment]

If this was a CI/CD thing then we would be able to see what happened over time. What was run, when it was run, what step happened when... Currently the automarker is pretty opaque.

8. Multi-part projects need DRY tests [DONE]

Currently, if there is a multi-part project we need to explicitly copy tests from one perfect project to the next. We should be able to extend things somehow.

9. No way to track performance of an automarker config over time. [TODO]

We can see reviews that were left, but we can't see when a user needed to step in and stop the process. This might be a hard thing to get right.

10. Self-test is a pain in the bum [TODO] 

It would be nice to be able to run a self-test for everything with a single command

11. Staff members were not in a good place to contribute or make use of the config since we needed to connect straight to the Tilde db [DONE]