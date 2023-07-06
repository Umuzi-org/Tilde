import re
import os
import sys
from importlib import import_module
from utils import (
    TAG_SETUP,
    TAG_RUNNING,
    TAG_RETURNED,
    TAG_IMPORT_LEARNER_CODE,
    TAG_COMMAND_DESCRIPTION,
)
from utils import AdapterCommandOutput


class TestRunner:
    def __init__(self, test_path):
        self.test_path = test_path
        self.results = {}
        # self.results stores the results of the test run. The format it:
        # {
        #   test_file_name_1: {
        #       test_name_1: [array of failed assertions],
        #       test_name_2: [], # empty array means the test passed
        #   },
        #  test_file_name_2: { ... },
        #  ...
        # }

    def has_errors(self):
        for test_file_name, test_results in self.results.items():
            for test_name, failed_assertions in test_results.items():
                if failed_assertions:
                    return True
        return False

    def run_command(self, command, assert_no_import_side_effects=True):
        """This function is called within individual tests. For example:

        command = get_adapter_shell_command()
        command_output = tester.run_command(command, assert_no_import_side_effects=False)
        """

        assert command, "command should not be empty"
        assert type(command) is str, "command must be a string"
        command_output = AdapterCommandOutput.run_command(command)
        self.assert_setup_empty(command_output)
        self.assert_command_description_present(command_output)
        self.assert_no_errors(command_output)
        if assert_no_import_side_effects:
            self.assert_no_import_side_effects(command_output)
        return command_output

    def run_tests(self, fail_fast):
        test_files = os.listdir(self.test_path)
        test_files = [s for s in test_files if re.match(r"^test_.*\.py$", s)]

        sys.path.append(str(self.test_path.resolve()))
        for s in sys.path:
            print(s)

        for file_name in test_files:
            self.set_test_file_name(file_name)
            file_name = file_name[:-3]  # remove the .py extension

            try:
                module = import_module(file_name)
            except ImportError as e:
                raise SystemError(
                    f"Error importing {file_name}: {e}\nThe problem is likely that the functional tests dont include the module reload boilerplate"
                )

            function_names = [s for s in dir(module) if s.startswith("test_")]
            for name in function_names:
                test_function = getattr(module, name)
                if type(test_function).__name__ != "function":
                    continue
                self.set_test_name(name)
                test_function(self)
                if fail_fast and self.has_errors():
                    return

        sys.path.pop(sys.path.index(str(self.test_path.resolve())))

    def set_test_file_name(self, test_file_name):
        print(f"running test file: {test_file_name}...")
        self.test_file_name = test_file_name
        self.results[self.test_file_name] = {}

    def set_test_name(self, test_name):
        print(f"\tRunning test: {test_name}...")
        self.test_name = test_name
        self.results[self.test_file_name][test_name] = []

    def register_test_error(self, command_description, error_message):
        self.results[self.test_file_name][self.test_name].append(
            {"error_message": error_message, "command_description": command_description}
        )

    def assert_command_description_present(self, command_output):
        assert command_output[
            TAG_COMMAND_DESCRIPTION
        ], f"expected command description to be present\n\nstderr={command_output.stderr}\n\nstdout={command_output.stdout}"

    def assert_setup_empty(self, command_output):
        assert command_output[TAG_SETUP] in (
            "",
            None,
        ), f"expected setup to have no output but got:\n\n{command_output[TAG_SETUP]}\n\nstderr={command_output.stderr}\n\nstdout={command_output.stdout}"  # this is a sanity check for us, not a test of the user

    def assert_no_import_side_effects(self, command_output):
        if command_output[TAG_IMPORT_LEARNER_CODE]:
            self.register_test_error(
                command_output.command_description,
                f"When we imported your code then there were unexpected side effects. For code to be as useful and reusable as possible it should be safe to import. So importing should not call functions or print anything.\n\nHere is what your code printed out when we imported it:\n\n{command_output[TAG_IMPORT_LEARNER_CODE]}",
            )

    def assert_no_errors(self, command_output):
        if command_output.stderr:
            self.register_test_error(
                command_output.command_description,  # red flag
                f"Your code produced an error when we tried to run it. This is very bad because it means you didn't try to run your code before you handed it in.\n\nHere is the error message\n\n{command_output.stderr}",
            )

    def assert_returned(self, command_output, expected, sort_key=None):
        returned = command_output[TAG_RETURNED]

        if sort_key:
            returned = sorted(returned, key=sort_key)
            expected = sorted(expected, key=sort_key)

        if returned != expected:
            self.register_test_error(
                command_output.command_description,
                f"Your code returned the wrong value. It returned `{command_output[TAG_RETURNED]}` but we expected `{expected}`",
            )

    def assert_printed(self, command_output, expected):
        printed = command_output[TAG_RUNNING]
        if printed != expected:
            self.register_test_error(
                command_output.command_description,
                f"Your code printed the wrong value. It printed `{command_output[TAG_RUNNING]}` but we expected `{expected}`",
            )
