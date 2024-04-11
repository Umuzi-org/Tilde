from django.test import TestCase
from automarker_app.lib.automarker_test_runner import JavaScriptTestRunner
from automarker_app.lib.utils import AdapterCommandOutput


class TestAutomarkerTestRunnerForJavascript(TestCase):
    def test_get_error_type_and_message_single_line_message(self):
        runner = JavaScriptTestRunner(test_path="", clone_dir_path="")
        runner.last_command_output = AdapterCommandOutput(
            stdout="",
            stderr="""/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/src/consume_github_api.js:35
            throw new Error(check.error);
                ^

    Error: User not found: GregBerryGreenMamba
        at checkIfUserOrRepoExists (/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/src/consume_github_api.js:35:15)
        at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
        at async getPullRequests (/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/src/consume_github_api.js:5:3)
        at async runAsyncFunction (/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/functional_tests/adapter/get_pull_requests.js:23:18)

    Node.js v19.0.1

    """,
        )
        error_type, error_message = runner.get_error_type_and_message()
        assert error_type == "Error"
        assert error_message == "User not found: GregBerryGreenMamba"

    def test_get_error_type_and_message_multi_line_message(self):
        runner = JavaScriptTestRunner(test_path="", clone_dir_path="")
        runner.last_command_output = AdapterCommandOutput(
            stdout="",
            stderr="""/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/src/consume_github_api.js:35
            throw new Error(check.error);
                ^

    Error: User not found: GregBerryGreenMamba
    more stuff
        even more
        at checkIfUserOrRepoExists (/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/src/consume_github_api.js:35:15)
        at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
        at async getPullRequests (/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/src/consume_github_api.js:5:3)
        at async runAsyncFunction (/home/sheena/workspace/Tilde/automarker_2/gitignore/186-javascript-perfect/functional_tests/adapter/get_pull_requests.js:23:18)

    Node.js v19.0.1

    """,
        )
        error_type, error_message = runner.get_error_type_and_message()
        assert error_type == "Error"
        assert (
            error_message
            == "User not found: GregBerryGreenMamba\nmore stuff\n    even more"
        )
