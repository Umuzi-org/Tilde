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
import subprocess
from constants import (
    STEP_STATUS_PASS,
    STEP_STATUS_RED_FLAG,
    STEP_STATUS_NOT_YET_COMPETENT,
)


class _TestRunner:
    class _BaseTestException(Exception):
        def __init__(self, message, status):
            self.message = message
            self.status = status
            super().__init__(message)

    class StopTestFunctionException(_BaseTestException):
        """This is raised if there is some kind of unrecoverable error while running an individual test function. Eg if there is an error in running the learner's code then there is no point checking if the function returned the right thing."""

    class StopTestSuiteException(_BaseTestException):
        """This is raised if there is no reason to continue running the test suite. Eg if there is an error in the setup then there is no point running the tests."""

    def __init__(self, test_path, clone_dir_path):
        self.clone_dir_path = clone_dir_path
        self.test_path = test_path

        # the following attributes are used internally

        self.test_file_name = (
            None  # the name of the file containing the tests we are currently running
        )
        self.test_name = None  # the name of the test we are currently running
        self.last_command_output = None
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

    def sanitize_stderr(self):
        """the stderr from the subprocess is likely to contain information about the automarker test environment. This method removes that information from the stderr.

        Override this in child classes if necessary.
        """
        return self.last_command_output.stderr

    def status(self):
        if self.has_errors():
            # look through failures, if any are red flags then return red flag else return Not yet competent
            for test_file_name, test_results in self.results.items():
                for test_name, failed_assertions in test_results.items():
                    for assertion in failed_assertions:
                        if assertion["status"] == STEP_STATUS_RED_FLAG:
                            return STEP_STATUS_RED_FLAG
                return STEP_STATUS_NOT_YET_COMPETENT
        return STEP_STATUS_PASS

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
        try:
            self.last_command_output = AdapterCommandOutput.run_command(command)
        except subprocess.TimeoutExpired:
            raise self.StopTestSuiteException(
                "Your code took too long to run. Are you sure you don't have any infinite loops? Make sure that you can run your own code"
            )

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
            for name in function_names:
                test_function = getattr(module, name)
                if type(test_function).__name__ != "function":
                    continue
                self.set_test_name(name)
                try:
                    test_function(self)
                except self.StopTestFunctionException as e:
                    self.register_test_error(error_message=e.message, status=e.status)
                    # once we have logged the error er move onto the next test
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

    def register_test_error(self, error_message, status=STEP_STATUS_NOT_YET_COMPETENT):
        self.results[self.test_file_name][self.test_name].append(
            {
                "error_message": error_message,
                "command_description": self.last_command_output.command_description,
                "status": status,
            }
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
                f"When we imported your code then there were unexpected side effects. For code to be as useful and reusable as possible it should be safe to import. So importing should not call functions or print anything.\n\nHere is what your code printed out when we imported it:\n\n{self.last_command_output[TAG_IMPORT_LEARNER_CODE]}",
            )

    def assert_no_errors(self):
        if self.last_command_output.stderr:
            raise self.StopTestFunctionException(
                f"Your code produced an error when we tried to run it. This is very bad because it means your code doesn't run under normal conditions.\n\nHere is the error message\n\n{self.sanitize_stderr()}",
                status=STEP_STATUS_NOT_YET_COMPETENT,
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
                    f"{message} It seems that you returned the wrong datatype. Note that the ordering of the elements doesn't matter in this case.",
                )
                return
            expected = sorted(expected, key=sort_key)

        if returned != expected:
            self.register_test_error(
                message,
            )

    def assert_printed(self, expected):
        printed = self.last_command_output[TAG_RUNNING]
        if printed != expected:
            self.register_test_error(
                f"Your code printed the wrong value. It printed `{self.last_command_output[TAG_RUNNING]}` but we expected `{expected}`",
            )


class PythonTestRunner(_TestRunner):
    def assert_no_import_errors(self):
        if TAG_IMPORT_LEARNER_CODE in self.last_command_output.unfinished_tags():
            stderr = self.last_command_output.stderr
            assert stderr, "there should be an error"
            if "ModuleNotFoundError" in stderr:
                error = re.search(r"\n(ModuleNotFoundError.*')\n", stderr).groups()[0]
                raise self.StopTestFunctionException(
                    f"There was an error importing your code. Please make sure you've named everything correctly. Here is the error message: `{error}`",
                    status=STEP_STATUS_NOT_YET_COMPETENT,
                )

            if "ImportError" in stderr:
                error = re.search(r"\n(ImportError.*) \(.*\n", stderr).groups()[0]
                raise self.StopTestFunctionException(
                    f"There was an error importing your code. Please make sure you've named everything correctly. Here is the error message: `{error}`",
                    status=STEP_STATUS_NOT_YET_COMPETENT,
                )
            if "Traceback" in stderr:
                # get the index of the last time the word File was mentioned in stderr

                raise self.StopTestFunctionException(
                    f"There was a fatal error while importing your code. This is very bad because your code is completely unusable. Make sure you can run your own code before you hand it in. `{self.sanitize_stderr()}`",
                    status=STEP_STATUS_RED_FLAG,
                )

            raise NotImplementedError()

    def sanitize_stderr(self):
        """The traceback will include a bunch of ifo about our test environment. Remove this so we can show the learner the important stuff without confusing them"""
        stderr = self.last_command_output.stderr
        index = stderr.rindex("File")
        stderr = stderr[index:]
        clone_path = str(self.clone_dir_path.resolve())
        stderr = stderr.replace(clone_path, "")
        return stderr


class JavaTestRunner(_TestRunner):
    def assert_no_import_errors(self):
        # there can't be import errors in Java projects. The errors will come up during build.
        pass

    def sanitize_stderr(self):
        stderr = self.last_command_output.stderr

        first_at = stderr.index("\n\tat ")

        while stderr.rindex("\n\tat ") != first_at:
            stderr = stderr[: stderr.rindex("\n\tat ")]
        return stderr


class JavaScriptTestRunner(_TestRunner):
    def assert_no_import_errors(self):
        stderr = self.last_command_output.stderr
        unfinished_tags = self.last_command_output.unfinished_tags()

        if TAG_IMPORT_LEARNER_CODE in unfinished_tags:
            assert stderr, "there should be an error"

            if "Error: Cannot find module" in stderr:
                error = re.search(
                    r"(Error: Cannot find module '.*')\n", stderr
                ).groups()[0]
                error = error.replace("../", "")

                raise self.StopTestFunctionException(
                    f"There was an error importing your code. Please make sure you've named everything correctly. Here is the error message:\n`{error}`",
                    status=STEP_STATUS_NOT_YET_COMPETENT,
                )
            if "Error" in stderr:
                error = re.search(r"\n(.*Error.*)\n", stderr).groups()[0]
                raise self.StopTestFunctionException(
                    f"There was an error importing your code. Your code is completely unrunnable! Please make sure you can actually run your code before handing it in. Here is the error message:\n`{self.sanitize_stderr()}`",
                    status=STEP_STATUS_RED_FLAG,
                )

            raise NotImplementedError()

        if TAG_RUNNING in unfinished_tags:
            found = re.search(r"(TypeError: .* is not a function)\n", stderr)
            if found:
                error = found.groups()[0]
                raise self.StopTestFunctionException(
                    f"There was an error running your code. Please make sure you've named everything correctly. Here is the error message: `{error}`",
                    status=STEP_STATUS_NOT_YET_COMPETENT,
                )

    def sanitize_stderr(self):
        stderr = self.last_command_output.stderr
        stderr = stderr.split("at Object")[0].strip()
        stderr = stderr.replace(str(self.clone_dir_path.resolve()), "")
        stderr = "\n".join([s for s in stderr.split("\n") if s])
        return stderr
