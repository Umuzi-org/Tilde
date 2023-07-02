import subprocess
import re
import json

TAG_SETUP = "setup"
TAG_IMPORT_LEARNER_CODE = "import_learner_code"
TAG_RUNNING = "running"
TAG_RETURNED = "returned"
TAG_COMMAND_DESCRIPTION = "command_description"

output_tags = [
    TAG_SETUP,
    TAG_IMPORT_LEARNER_CODE,
    TAG_RUNNING,
    TAG_RETURNED,
    TAG_COMMAND_DESCRIPTION,
]


class CommandOutput:
    """A class to hold the output of a command. It has attributes for each of the tags in output_tags. It also stores stdout and stderr as attributes.

    The value passed in as returned is converted to a python object using json.loads() and stored as an attribute called returned.
    """

    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

        tagged_output = self.process_std_out_tags(stdout)

        for tag in output_tags:
            self.__setattr__(tag, None)

        for k, v in tagged_output.items():
            self.__setattr__(k, v)
        if TAG_RETURNED in tagged_output:
            returned = tagged_output[TAG_RETURNED].strip()

            if returned == "undefined":
                self.returned = None
            if not returned:
                self.returned = None
            else:
                self.returned = json.loads(returned)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __repr__(self):
        return f"CommandOutput({self.__dict__})"

    def process_std_out_tags(self, stdout):
        result = {}
        for tag in output_tags:
            found = re.search(rf"<{tag}>(.+?)</{tag}>", stdout, re.DOTALL)
            if found:
                result[tag] = found.groups()[0].strip()
        return result


def get_command_output(command):
    output = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout = output.stdout.decode("utf-8")
    stderr = output.stderr.decode("utf-8")

    if stdout == "":
        if stderr != "":
            raise Exception(
                f"stderr is not empty when stdout is empty. Does the script exist? Or is it totally broken? \ncommand = `{command}`\nstderr: {stderr}"
            )
        else:
            raise Exception(
                f"stdout and stderr are both empty. Is the script implemented? \ncommand = `{command}`\nstdout: {stdout}\nstderr: {stderr}"
            )

    return CommandOutput(stdout=stdout, stderr=stderr)
