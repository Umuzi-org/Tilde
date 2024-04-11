from django.test import TestCase
from automarker_app.lib.automarker_test_runner import PythonTestRunner
from automarker_app.lib.utils import AdapterCommandOutput


class TestAutomarkerTestRunnerForPython(TestCase):
    def test_get_error_type_and_message_single_line_message(self):
        runner = PythonTestRunner(test_path="", clone_dir_path="")

        runner.last_command_output = AdapterCommandOutput(
            stdout="",
            stderr="""Traceback (most recent call last):
      File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/functional_tests/adapter/get_pull_requests.py", line 25, in <module>
        result = get_pull_requests(
      File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/src/consume_github_api.py", line 52, in get_pull_requests
        validate_owner_and_repo(owner, repo)
      File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/src/consume_github_api.py", line 45, in validate_owner_and_repo
        raise ValueError(f"User not found: '{owner}'.")
    ValueError: User not found: 'GregBerryGreenMamba'.

    # """,
        )

        error_type, error_message = runner.get_error_type_and_message()

        assert error_type == "ValueError"
        assert error_message == "User not found: 'GregBerryGreenMamba'."

    def test_get_error_type_and_message_multi_line_message(self):
        runner = PythonTestRunner(test_path="", clone_dir_path="")

        runner.last_command_output = AdapterCommandOutput(
            stdout="",
            stderr="""Traceback (most recent call last):
  File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/functional_tests/adapter/get_pull_requests.py", line 25, in <module>
    result = get_pull_requests(
  File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/src/consume_github_api.py", line 52, in get_pull_requests
    validate_owner_and_repo(owner, repo)
  File "/home/sheena/workspace/Tilde/automarker_2/gitignore/186-python-perfect/src/consume_github_api.py", line 45, in validate_owner_and_repo
    raise ValueError(f"User not found: '{owner}'.")
ValueError: User not found: 'GregBerryGreenMamba'.
some other context
    even more
""",
        )
        error_type, error_message = runner.get_error_type_and_message()
        assert error_type == "ValueError"
        assert (
            error_message
            == "User not found: 'GregBerryGreenMamba'.\nsome other context\n    even more"
        )
