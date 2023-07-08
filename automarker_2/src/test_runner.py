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


class _TestRunner:
    class _BaseTestException(Exception):
        def __init__(self, message, red_flag=False):
            self.message = message
            self.red_flag = red_flag  # TODO: use this
            super().__init__(message)

    class StopTestFunctionException(_BaseTestException):
        """This is raised if there is some kind of unrecoverable error while running an individual test function. Eg if there is an error in running the learner's code then there is no point checking if the function returned the right thing."""

    class StopTestSuiteException(_BaseTestException):
        """This is raised if there is no reason to continue running the test suite. Eg if there is an error in the setup then there is no point running the tests."""

    def __init__(self, test_path, clone_dir_path):
        self.clone_dir_path = clone_dir_path
        self.test_path = test_path
        self.results = {}
        self.last_command_output = None
        # self.results stores the results of the test run. The format it:
        # {
        #   test_file_name_1: {
        #       test_name_1: [array of failed assertions],
        #       test_name_2: [], # empty array means the test passed
        #   },
        #  test_file_name_2: { ... },
        #  ...
        # }

    def sanitize_stderr(self):
        """the stderr from the subprocess is likely to contain information about the automarker test environment. This method removes that information from the stderr.

        Override this in child classes if necessary.
        """
        return self.last_command_output.stderr

    def fail_results(self):
        """return details about the failing tests only"""
        failing_tests = {}
        for test_file_name, test_results in self.results.items():
            for test_name, failed_assertions in test_results.items():
                if failed_assertions:
                    failing_tests.setdefault(test_file_name, {})
                    failing_tests[test_file_name][test_name] = failed_assertions
        return failing_tests

    def has_errors(self):
        for test_file_name, test_results in self.results.items():
            for test_name, failed_assertions in test_results.items():
                if failed_assertions:
                    return True
        return False

    def run_command(
        self, command, assert_no_import_side_effects=True, assert_no_errors=True
    ):
        """This function is called within individual tests. For example:

        command = get_adapter_shell_command()
        command_output = tester.run_command(command, assert_no_import_side_effects=False)
        """

        assert command, "command should not be empty"
        assert type(command) is str, "command must be a string"
        self.last_command_output = AdapterCommandOutput.run_command(command)
        self.assert_setup_empty()
        self.assert_command_description_present()
        self.assert_no_import_errors()
        if assert_no_errors:
            self.assert_no_errors()
        if assert_no_import_side_effects:
            self.assert_no_import_side_effects()

    def run_tests(self, fail_fast):
        test_files = os.listdir(self.test_path)
        test_files = [s for s in test_files if re.match(r"^test_.*\.py$", s)]

        sys.path.append(str(self.test_path.resolve()))

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
            # breakpoint()
            for name in function_names:
                test_function = getattr(module, name)
                if type(test_function).__name__ != "function":
                    continue
                self.set_test_name(name)
                try:
                    test_function(self)
                except self.StopTestFunctionException as e:
                    self.register_test_error(
                        command_description=self.last_command_output.command_description,
                        error_message=e.message,
                    )
                    pass  # we simply move onto the next test
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

    def assert_command_description_present(self):
        assert self.last_command_output[
            TAG_COMMAND_DESCRIPTION
        ], f"expected command description to be present. There is something wrong with the automarker project configuration\n\nstderr={self.last_command_output.stderr}\n\nstdout={self.last_command_output.stdout}"

    def assert_setup_empty(self):
        assert self.last_command_output[TAG_SETUP] in (
            "",
            None,
        ), f"expected setup to have no output but got:\n\n{self.last_command_output[TAG_SETUP]}\n\nstderr={self.last_command_output.stderr}\n\nstdout={self.last_command_output.stdout}. There is something wrong with the automarker project configuration"  # this is a sanity check for us, not a test of the user

    def assert_no_import_side_effects(self):
        if self.last_command_output[TAG_IMPORT_LEARNER_CODE]:
            self.register_test_error(
                self.last_command_output.command_description,
                f"When we imported your code then there were unexpected side effects. For code to be as useful and reusable as possible it should be safe to import. So importing should not call functions or print anything.\n\nHere is what your code printed out when we imported it:\n\n{self.last_command_output[TAG_IMPORT_LEARNER_CODE]}",
            )

    def assert_no_errors(self):
        if self.last_command_output.stderr:
            raise self.StopTestFunctionException(
                f"Your code produced an error when we tried to run it. This is very bad because it means your code doesn't run under normal conditions.\n\nHere is the error message\n\n{self.sanitize_stderr()}"
            )
        return True

    def assert_returned(self, expected, sort_key=None):
        returned = self.last_command_output[TAG_RETURNED]

        message = f"Your code returned the wrong value. It returned `{self.last_command_output[TAG_RETURNED]}` but we expected `{expected}`."

        if sort_key:
            try:
                returned = sorted(returned, key=sort_key)
            except TypeError:
                # if we cant sort it then it means the learner returned the wrong datatype
                self.register_test_error(
                    self.last_command_output.command_description,
                    f"{message} It seems that you returned the wrong datatype. Note that the ordering of the elements doesn't matter in this case.",
                )
                return
            expected = sorted(expected, key=sort_key)

        if returned != expected:
            self.register_test_error(
                self.last_command_output.command_description,
                f"{message} Note that the ordering of the elements needs to be exactly the same.",
            )

    def assert_printed(self, expected):
        printed = self.last_command_output[TAG_RUNNING]
        if printed != expected:
            self.register_test_error(
                self.last_command_output.command_description,
                f"Your code printed the wrong value. It printed `{self.last_command_output[TAG_RUNNING]}` but we expected `{expected}`",
            )


class PythonTestRunner(_TestRunner):
    def assert_no_import_errors(self):
        if TAG_IMPORT_LEARNER_CODE in self.last_command_output.unfinished_tags():
            assert self.last_command_output.stderr, "there should be an error"
            if "ModuleNotFoundError" in self.last_command_output.stderr:
                error = re.search(
                    r"\n(ModuleNotFoundError.*')\n", self.last_command_output.stderr
                ).groups()[0]
                raise self.StopTestFunctionException(
                    f"There was an error importing your code. Please make sure you've named everything correctly. Here is the error message: `{error}`"
                )
            elif "ImportError" in self.last_command_output.stderr:
                error = re.search(
                    r"\n(ImportError.*) \(.*\n", self.last_command_output.stderr
                ).groups()[0]
                raise self.StopTestFunctionException(
                    f"There was an error importing your code. Please make sure you've named everything correctly. Here is the error message: `{error}`"
                )
            elif "Traceback" in self.last_command_output.stderr:
                # get the index of the last time the word File was mentioned in stderr

                raise self.StopTestFunctionException(
                    f"There was a fatal error while importing your code. This is very bad because your code is completely unusable. Make sure you can run your own code before you hand it in. `{self.sanitize_stderr()}`",
                    red_flag=True,
                )

            else:
                breakpoint()
                here
                # this shouldn't happen

    def sanitize_stderr(self):
        """The traceback will include a bunch of ifo about our test environment. Remove this so we can show the learner the important stuff without confusing them"""
        stderr = self.last_command_output.stderr
        index = stderr.rindex("File")
        stderr = self.last_command_output.stderr[index:]
        clone_path = str(self.clone_dir_path.resolve())
        stderr = stderr.replace(clone_path, "")
        return stderr


class JavaTestRunner(_TestRunner):
    def assert_no_import_errors(self):
        breakpoint()
        woo


class JavaScriptTestRunner(_TestRunner):
    def assert_no_import_errors(self):
        breakpoint()
        woo
