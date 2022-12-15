Having to go through the apis in order to do any kind of data science is a big pain in the bum. It's much nicer to connect straight to the database. And on top of this, it's pretty nice to be able to make use of the django models as they are.

Note that this does make use of VSCode's built-in jupyter features. This stuff wont work in the same way in a different editor.

# Setup your database proxy

Our data is in Google cloud SQL. To access it we use a proxy. That can be found inside: 

```
tilde/database/cloudsql
```

To start the proxy:

```
source path/to/where/you/like/to/keep/your/environmental_variables.sh  # replace this path with your path
./start_sql_proxy.sh
```

## What environmental variables?

Great question.

For the proxy to connect to google cloud it needs a few values.  You'll also need a few variables for the Python side of things. It's easiest to put all these variables in one file. Put that file somewhere safe.

If you commit this file or any credential key to git then the best thing to do would be:

- invalidate the keys and secrets (by interacting with Google cloud console)
- get some new secrets and be more careful for now on
- take a shower
- change your name and move to a small anonymous island off the coast of Thailand

Those last 2 steps are optional, but you might want to do them on account of the shame. 

# Setup vscode and python

## 1. Create a separate virtual environment just for your data wrangling. 

This is necessary because you're going to need to set that environment up with some credentials that you wont necessarily want to use most of the time.

```
mkvirtualenv tilde_3_9_jupyter -p $(which python3.9)
workon tilde_3_9_jupyter 

pip install -r requirements.txt
pip install -r data_requirements.txt

```

## 2. Update your activate script so that it loads up your database credentials.

To find your activate script do this:

```
workon tilde_3_9_jupyter # if it is not already active
which python
```

This will tell you the path to the python interpreter you are using. Eg it might look like this:

```
/home/username/.VirtualEnvs/tilde_3_9_jupyter/bin/python
```

The activate script is in the same directory as your python interpreter.  You can open the activate script for editing using a command like:

```
code /home/username/.VirtualEnvs/tilde_3_9_jupyter/bin/activate
```

Now you want to make sure that your credentials are available whenever you the activate script is evoked. There are 2 ways to do this:

1. Just add a bunch of export statements straight to your activate script:

```
export SECRET_NAME=whatever
```

Or

2. Create a separate sh file that contains all your exports and then source it in your activate script

```
source /path/to/your/very/own/script.sh
```

Option 2 is actually the nicest, it's more versatile.

## 3. Tell vscode which interpreter you want to use

Press Ctrl+Shift+P and start typing "Jupyter interpreter".
Select the option to "Select interpreter to start Jupyter server" and enter the path to your new python interpreter. 

It would be something like (but not exactly like) this:

```
/home/username/.VirtualEnvs/tilde_3_9_jupyter/bin/python
```

Again, you can find the path to your python interpreter by activating your virtualenv and then using `which python`

## 4. Execute proof_of_concept.py 

You should see it in `data_sciencing/proof_of_concept.py`. Just open the file in your vscode as if you want to edit it.

Click on the first block and then click on "Run Below" (it's on top of the block.) 

This will open an interactive window and, if all went well, you should see a dataframe head.

