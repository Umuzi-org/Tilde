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


def subprocess_run(command, timeout=60):
    # TODO: some things should take longer than others. Set a lower default for timeout and then increase it for certain commands
    output = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )

    stdout = output.stdout.decode("utf-8")
    stderr = output.stderr.decode("utf-8")

    return stdout, stderr


class AdapterCommandOutput:
    """A class to hold the output of a command. It has attributes for each of the tags in output_tags. It also stores stdout and stderr as attributes.

    The value passed in as returned is converted to a python object using json.loads() and stored as an attribute called returned.
    """

    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

        tagged_output = self._process_std_out_tags(stdout)

        for tag in output_tags:
            self.__setattr__(tag, None)

        for k, v in tagged_output.items():
            self.__setattr__(k, v)
        if TAG_RETURNED in tagged_output:
            returned = tagged_output[TAG_RETURNED].strip()

            if returned == "undefined":
                self.returned = None
            elif not returned:
                self.returned = None
            else:
                self.returned = json.loads(returned)

    def unfinished_tags(self):
        """Return a list of tags that were opened but not closed in the stdout."""
        result = []
        for tag in output_tags:
            if (f"<{tag}>" in self.stdout) and (f"</{tag}>" not in self.stdout):
                result.append(tag)
        return result

    def repeating_tags(self):
        """Return a list of tags that were opened more than once in the stdout."""
        result = []
        for tag in output_tags:
            if self.stdout.count(f"<{tag}>") > 1:
                result.append(tag)
        return result

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __repr__(self):
        return f"CommandOutput({self.__dict__})"

    @staticmethod
    def _clean_tag_content(content):
        """
        - remove blank lines from the beginning and end (not the middle)
        - remove blank space from the ends of lines
        """
        clean_lines = []
        for line in content.rstrip().split("\n"):
            stripped = line.rstrip()
            if not clean_lines:
                # whitespace lines are removed
                if stripped == "":
                    continue
            clean_lines.append(stripped)
        result = "\n".join(clean_lines)
        return result

    def _process_std_out_tags(self, stdout):
        result = {}
        for tag in output_tags:
            found = re.search(rf"<{tag}>(.+?)</{tag}>", stdout, re.DOTALL)
            if found:
                content = found.groups()[0].rstrip()
                result[tag] = self._clean_tag_content(content)
        return result

    @classmethod
    def run_command(Cls, command):
        stdout, stderr = subprocess_run(command)

        if stdout == "":
            if stderr != "":
                raise Exception(
                    f"stderr is not empty when stdout is empty. Does the script exist? Or is it totally broken? \ncommand = `{command}`\nstderr: {stderr}"
                )
            else:
                raise Exception(
                    f"stdout and stderr are both empty. Is the script implemented? \ncommand = `{command}`\nstdout: {stdout}\nstderr: {stderr}"
                )

        return Cls(stdout=stdout, stderr=stderr)


def test_runner_expects_code_imports(cls):
    class NewRunnerCls(cls):
        def assert_import_learner_code_present(self):
            assert bool(
                re.search(
                    rf"<{TAG_IMPORT_LEARNER_CODE}>", self.last_command_output.stdout
                )
            ), f"expected <{TAG_IMPORT_LEARNER_CODE}> to be present. There is something wrong with the automarker project configuration.\n\nstderr={self.last_command_output.stderr}\n\nstdout={self.last_command_output.stdout}"

    return NewRunnerCls
