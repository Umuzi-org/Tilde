import os
from pathlib import Path
import re
import sys
from importlib import import_module
from exceptions import SystemError
import json

# from exceptions import SystemError
from utils import TAG_SETUP, TAG_RUNNING, TAG_RETURNED, TAG_IMPORT_LEARNER_CODE


class Clone:
    name = "clone"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        if clone_dir_path.exists():
            os.system(f"rm -rf {clone_dir_path}")
            assert clone_dir_path.exists() is False

        if self_test:
            os.system(f"cp -r {project_uri} {clone_dir_path}")
        else:
            os.system(f"git clone {project_uri} {clone_dir_path}")

        if not clone_dir_path.exists():
            raise SystemError(
                "Clone not successful",
                project_uri=project_uri,
                clone_dir_path=clone_dir_path,
                self_test=self_test,
                config=config.__file__,
            )


class PrepareFunctionalTests:
    """Copy the adapter and tests into the right place so we can run them. The final directory structure will look like:

    clone_dir_path/
        agnostic_tests/
            adapter/
                adapter.py  # this will allow you to call the learner code like a python function
            test_*.py # these are the tests

    """

    name = "preparation"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_path = Path(config.__file__).parent.parent / "agnostic_tests"
        os.system(f"cp -r {test_path} {clone_dir_path}")

        adapter_path = Path(config.__file__).parent / "adapter"
        os.system(f"cp -r {adapter_path} {clone_dir_path/'agnostic_tests'}")


class RunFunctionalTests:
    name = "running functional tests"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_path = clone_dir_path / "agnostic_tests"

        runner = TestRunner(test_path)
        runner.run_tests(fail_fast)

        print("Errors")
        print(json.dumps(runner.results, sort_keys=True, indent=4))
        print("TODO")


class TestRunner:
    def __init__(self, test_path):
        self.results = {}
        self.test_path = test_path

    def run_tests(self, fail_fast):
        test_files = os.listdir(self.test_path)
        test_files = [s for s in test_files if re.match(r"^test_.*\.py$", s)]

        sys.path.append(str(self.test_path.resolve()))

        for file_name in test_files:
            self.set_test_file_name(file_name)
            file_name = file_name[:-3]  # remove .py
            module = import_module(file_name)
            function_names = [s for s in dir(module) if s.startswith("test_")]
            for name in function_names:
                test_function = getattr(module, name)
                if type(test_function).__name__ != "function":
                    continue
                self.set_test_name(name)
                test_function(self)
                if fail_fast and self.results:
                    return

        sys.path = sys.path[:-1]

    def set_test_file_name(self, test_file_name):
        print(f"running test file: {test_file_name}...")
        self.test_file_name = test_file_name

    def set_test_name(self, test_name):
        print(f"\tRunning test: {test_name}...")
        self.test_name = test_name

    def register_test_error(self, call_description, error_message):
        # print(f"\t\tError")
        self.results[self.test_file_name] = self.results.get(self.test_file_name, {})
        self.results[self.test_file_name][self.test_name] = self.results[
            self.test_file_name
        ].get(self.test_name, [])

        self.results[self.test_file_name][self.test_name].append(
            error_message
        )  # TODO and call_description

    def assert_setup_empty(self, command_output):
        assert (
            command_output[TAG_SETUP] == ""
        ), f"expected setup to have no output but got:\n\n{command_output[TAG_SETUP]}\n\nstderr={command_output.stderr}\n\nstdout={command_output.stdout}"  # this is a sanity check for us, not a test of the user

    def assert_no_import_side_effects(self, command_output):
        if command_output[TAG_IMPORT_LEARNER_CODE] != "":
            self.register_test_error(
                "call_description TODO",
                "When we imported your code then there were unexpected side effects. For code to be as useful and reusable as possible it should be safe to import. So importing should not call functions or print anything.\n\nHere is what your code printed out when we imported it:\n\n{command_output[TAG_IMPORT_LEARNER_CODE]}",
            )

    def assert_no_errors(self, command_output):
        if command_output.stderr:
            self.register_test_error(
                "call_description TODO",  # red flag
                f"Your code produced an error when we tried to run it. This is very bad because it means you didn't try to run your code before you handed it in.\n\nHere is the error message\n\n{command_output.stderr}",
            )

    def assert_returned(self, command_output, expected, sort_key=None):
        returned = command_output[TAG_RETURNED]

        if sort_key:
            returned = sorted(returned, key=sort_key)
            expected = sorted(expected, key=sort_key)

        if returned != expected:
            self.register_test_error(
                "call_description TODO",
                f"Your code returned the wrong value. It returned {command_output[TAG_RETURNED]} but we expected {expected}",
            )
