import re
import os
import sys
from importlib import import_module
import subprocess

from .utils import (
    TAG_SETUP,
    TAG_RUNNING,
    TAG_RETURNED,
    TAG_IMPORT_LEARNER_CODE,
    TAG_COMMAND_DESCRIPTION,
    AdapterCommandOutput,
    test_runner_expects_code_imports,
)
from .constants import (
    STEP_STATUS_PASS,
    STEP_STATUS_RED_FLAG,
    STEP_STATUS_NOT_YET_COMPETENT,
)


class _TestRunner:
    EXCEPTION_OR_ERROR = "EXCEPTION_OR_ERROR NOT SET!!"
    RAISE_OR_THROW = "RAISE_OR_THROW NOT SET!!"

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

        # used for marking written word projects

    def get_error_type_and_message(self):
        """
        look at the stderr of the last command run and return a tuple containing the error type and error message. This should be the error that was raised or thrown. This is typically used when checking that the learner raised an appropriate error
        """
        raise NotImplementedError()

    def sanitize_stderr(self):
        """the stderr from the subprocess is likely to contain information about the automarker test environment. This method removes that information from the stderr.

        Override this in child classes if necessary.
        """
        raise NotImplementedError()

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
        self.assert_running_tag_present()
        self.assert_no_repeated_tags()
        self.assert_import_learner_code_present()
        self.assert_no_import_errors()
        if assert_no_errors:
            self.assert_no_errors()
        if assert_no_import_side_effects:
            self.assert_no_import_side_effects()

    def run_tests(self, fail_fast):
        """
        returns the number of test files that were visited
        """
        test_files = os.listdir(self.test_path)
        test_files = [s for s in test_files if re.match(r"^test_.*\.py$", s)]

        sys.path.append(str(self.test_path.resolve()))

        for i, file_name in enumerate(test_files):
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
                    return i + 1
        return len(test_files)

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
                "command_description": self.last_command_output.command_description
                if self.last_command_output
                else None,
                "status": status,
            }
        )

    def assert_command_description_present(self):
        assert self.last_command_output[
            TAG_COMMAND_DESCRIPTION
        ], f"expected command description to be present. There is something wrong with the automarker project configuration\n\nstderr={self.last_command_output.stderr}\n\nstdout={self.last_command_output.stdout}"

    def assert_running_tag_present(self):
        assert bool(
            re.search(rf"<{TAG_RUNNING}>", self.last_command_output.stdout)
        ), f"expected <{TAG_RUNNING}> to be present. There is something wrong with the automarker project configuration.\n\nstderr={self.last_command_output.stderr}\n\nstdout={self.last_command_output.stdout}"

    def assert_no_repeated_tags(self):
        if len(self.last_command_output.repeating_tags()):
            assert (
                False
            ), f"expected no repeating tags but the following tags appear more than once: {self.last_command_output.repeating_tags()}"

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

    def get_returned(self):
        return self.last_command_output[TAG_RETURNED]

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

    def assert_equal(self, actual, expected, message):
        if actual != expected:
            self.register_test_error(
                message,
            )

    def assert_printed(self, expected):
        printed = self.last_command_output[TAG_RUNNING]
        if printed != str(expected):
            self.register_test_error(
                f"Your code printed the wrong value. It printed\n```\n{self.last_command_output[TAG_RUNNING]}\n```\nbut we expected\n```\n{expected}\n```",
            )

    def assert_similar_error_message_raised(self, similar_message, max_distance):
        stderr = self.last_command_output.stderr
        if not stderr:
            raise self.StopTestFunctionException(
                f"There was meant to be an {self.EXCEPTION_OR_ERROR} but there wasn't one. Make sure you remember to {self.RAISE_OR_THROW} an {self.EXCEPTION_OR_ERROR} when you need to. If you are {self.RAISE_OR_THROW} the {self.EXCEPTION_OR_ERROR} then the problem might be that you are catching it as well. Don't catch {self.EXCEPTION_OR_ERROR}s unless you are doing something very specific and intentional with them. Errors should never pass silently. Unless explicitly silenced."
            )
        error_type, error_message = self.get_error_type_and_message()

        if similar_message:
            from automarker_app.lib.ai_helpers import (
                similarity_distance,
            )  # just in time import because this thing is slow

            distance = similarity_distance(similar_message, error_message)
            if distance > max_distance:
                raise self.StopTestFunctionException(
                    f"Your error message is not descriptive enough, or it is describing the wrong thing. A suitable error message is `{similar_message}`. Yours is `{error_message}`.",
                    status=STEP_STATUS_NOT_YET_COMPETENT,
                )


@test_runner_expects_code_imports
class PythonTestRunner(_TestRunner):
    EXCEPTION_OR_ERROR = "Exception"
    RAISE_OR_THROW = "raise"

    def assert_no_import_errors(self):
        # example stderr = 'Traceback (most recent call last):\n  File "/home/sheena/workspace/Tilde/automarker_2/gitignore/224-python-perfect/functional_tests/adapter/dog_sound.py", line 27, in <module>\n    from animals.animals import Dog\nModuleNotFoundError: No module named \'animals.animals\'; \'animals\' is not a package\n'

        if TAG_IMPORT_LEARNER_CODE in self.last_command_output.unfinished_tags():
            stderr = self.last_command_output.stderr
            assert stderr, "there should be an error"
            if "ModuleNotFoundError" in stderr:
                # error = re.search(r"\n(ModuleNotFoundError.*')\n", stderr).groups()[0]
                l = [s for s in stderr.split("\n") if "ModuleNotFoundError" in s]
                assert len(l) == 1
                error = l[0]

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

    def get_error_type_and_message(self):
        """
        Python tracebacks have a format like this:

        Traceback (most recent call last):
        File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/functional_tests/adapter/get_pull_requests.py", line 25, in <module>
            result = get_pull_requests(
        File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/src/consume_github_api.py", line 52, in get_pull_requests
            validate_owner_and_repo(owner, repo)
        File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/src/consume_github_api.py", line 45, in validate_owner_and_repo
            raise ValueError(f"User not found: '{owner}'.")
        ValueError: User not found: 'GregBerryGreenMamba'.
        some other context
            even more

        We want to extract the error type and the error message. So everything from the line that says "ValueError: ..." is relevant
        """
        stderr = self.last_command_output.stderr.strip()
        start_line = re.search(r"\n([A-Za-z].*: .*)", stderr).groups()[0]
        final_error = stderr[stderr.index(start_line) :]
        split_at = final_error.index(": ")
        error_type = final_error[:split_at]
        error_message = final_error[split_at + 2 :]

        return error_type, error_message


class JavaTestRunner(_TestRunner):
    EXCEPTION_OR_ERROR = "Exception"
    RAISE_OR_THROW = "throw"

    def assert_no_import_errors(self):
        # there can't be import errors in Java projects. The errors will come up during build.
        pass

    def assert_import_learner_code_present(self):
        # No import learner code tag in Java projects
        pass

    def sanitize_stderr(self):
        stderr = self.last_command_output.stderr

        first_at = stderr.index("\n\tat ")

        while stderr.rindex("\n\tat ") != first_at:
            stderr = stderr[: stderr.rindex("\n\tat ")]
        return stderr

    def get_error_type_and_message(self):
        error_info = self.last_command_output.stderr.strip().split("\n\tat ")[0]
        # Exception in thread "main" java.lang.IllegalArgumentException: Pet cannot be adopted again
        # at Home.adoptPet(Home.java:14)
        # at HomeAdoptAndSounds.main(HomeAdoptAndSounds.java:37)
        error_type = error_info.split(":")[0].split()[-1]
        error_message = ":".join(error_info.split(":")[1:]).strip()

        return error_type, error_message


@test_runner_expects_code_imports
class JavaScriptTestRunner(_TestRunner):
    EXCEPTION_OR_ERROR = "Error"
    RAISE_OR_THROW = "throw"

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

    def get_error_type_and_message(self):
        stderr = self.last_command_output.stderr.strip()
        start_line = re.search(r"\n([A-Za-z].*: .*)", stderr).groups()[0]
        end_line = re.search(r"(\n    at .* \(.*\))", stderr).groups()[0]

        final_error = stderr[stderr.index(start_line) : stderr.index(end_line)]
        split_at = final_error.index(": ")
        error_type = final_error[:split_at]
        error_message = final_error[split_at + 2 :]

        return error_type, error_message

    def assert_import_learner_code_present(self):
        assert bool(
            re.search(rf"<{TAG_IMPORT_LEARNER_CODE}>", self.last_command_output.stdout)
        ), f"expected <{TAG_IMPORT_LEARNER_CODE}> to be present. There is something wrong with the automarker project configuration.\n\nstderr={self.last_command_output.stderr}\n\nstdout={self.last_command_output.stdout}"


class MarkdownTestRunner(PythonTestRunner):
    def __init__(self, test_path, clone_dir_path):
        super().__init__(test_path, clone_dir_path)
        self.markdown_question = ""
        self.markdown_answer = ""
        self.question_number = None

    def assert_question_is(self, expected_question):
        if self.markdown_question.lower() == expected_question.lower():
            return
        from automarker_app.lib.ai_helpers import (
            similarity_distance,
        )  # just in time import because this thing is slow

        distance = similarity_distance(expected_question, self.markdown_question)
        if distance > 0.1:
            self.register_test_error(
                f"The question in your markdown file doesn't match the one in the instructions. The expected question is `{expected_question}`. Yours is `{self.markdown_question}`.",
                status=STEP_STATUS_NOT_YET_COMPETENT,
            )

    def get_question_and_answer_from_markdown_file(self, question_number):
        """This is used to mark markdown files. The files are named like: question_{number}.md and are formatted as follows:

        ```
        # Question

        the question

        # Answer

        the answer
        ```
        """
        self.question_number = question_number
        file_path = self.test_path.parent / f"question_{question_number}.md"
        assert file_path.exists()
        contents = file_path.read_text().strip()
        lines = contents.split("\n")
        assert lines[0].lower().startswith("# question")
        lines = lines[1:]

        for i, line in enumerate(lines):
            if line.lower().startswith("# answer"):
                self.markdown_question = "\n".join(lines[:i]).strip()
                self.markdown_answer = "\n".join(lines[i + 1 :]).strip()
                break

        if self.markdown_question == "":
            self.register_test_error(
                f"Your question_{question_number}.md file is meant to have a question and an answer in it. The expected format is as follows:\n\n```\n# Question\n\nthe question\n\n# Answer\n\nthe answer\n``` Please fix your file and resubmit your work.",
                status=STEP_STATUS_RED_FLAG,
            )

        # if self.markdown_answer == "":

    def assert_answer_like(self, answers_and_hints, min_matches):
        if self.markdown_answer == "":
            self.register_test_error(
                f"Question {self.question_number} has no answer! Are you sure you submitted your work according to the instructions?",
                status=STEP_STATUS_RED_FLAG,
            )
            return

        # lazy import on purpose
        import spacy
        import pandas as pd
        from automarker_app.lib.ai_helpers import embed_sentence, distance_functions

        max_distance = 0.075
        get_distance = distance_functions["cosine"]
        maximum_hints = (
            4  # if the learner got things wrong then give them at most this many hints
        )

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.markdown_answer)

        # get all the individual sentences from the learner's answer.
        sentences = [s.text for s in doc.sents]

        # sometimes meaning is spread over multiple sentences so we also want to consider adjacent sentences
        adjacent_sentences = [
            " ".join(sentences[i : i + 2]) for i in range(len(sentences) - 1)
        ]

        sentences.extend(adjacent_sentences)

        sentence_vectors = [embed_sentence(s) for s in sentences]

        df = pd.DataFrame(
            columns=["learner_sentence", "concept", "hint", "distance"],
        )
        for concept, hint in answers_and_hints:
            concept_vector = embed_sentence(
                concept
            )  # we could pre-embed these sentences and store it in a vector db to save some time
            for sentence, sentence_vector in zip(sentences, sentence_vectors):
                distance = get_distance(sentence_vector, concept_vector)
                df.loc[len(df)] = [
                    sentence.replace(
                        ";", ""
                    ),  # remove semicolons because they mess up any csv dumps
                    concept.replace(";", ","),
                    hint,
                    distance,
                ]

        df = df.sort_values(by=["distance"], ascending=True)
        # df.to_csv("gitignore/df_with_duplicates.csv")

        df = df.drop_duplicates(subset=["concept"], keep="first")
        # df.to_csv("gitignore/df_no_duplicates.csv")

        # each concept is represented once
        assert len(df) == len(answers_and_hints)

        df_matched = df[df["distance"] <= max_distance]
        matched_count = len(df_matched)

        print(f"*** matched {matched_count} concepts")
        if matched_count >= min_matches:
            return

        # the learner didn't match on enough concepts. Give them some hints
        # we aim for twice as many hints as the learner needs, but we don't want to just give them all the hints all at once so we cap it at maximum_hints
        hint_count = min(2 * (min_matches - matched_count), maximum_hints)

        df_unmatched = df[df["distance"] > max_distance]

        # get the last hint_count rows. We grab from the bottom because learners are more likely to have missed the last few concepts than the first few
        df_hints = df_unmatched.tail(hint_count)

        hints = df_hints["hint"].tolist()

        self.register_test_error(
            f"It looks like you haven't answered the question correctly or you haven't answered it in enough detail. Here are some hints to help you. Try to talk about the following:\n\n- "
            + "\n- ".join(hints),
            status=STEP_STATUS_NOT_YET_COMPETENT,
        )
