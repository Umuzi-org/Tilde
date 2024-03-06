from django.test import TestCase
from automarker_app.lib.automarker_test_runner import JupyterTestRunner
from automarker_app.lib.utils import AdapterCommandOutput


class TestAutomarkerTestRunnerForJupyter(TestCase):
    def test_error_messages_are_properly_interpreted(self):
        runner = JupyterTestRunner(test_path="", clone_dir_path="")

        runner.last_command_output = AdapterCommandOutput(
            stdout="""<setup>
</setup>
<command_description>
run the whole data_wrangling.ipynb notebook, and get the columns of the dataframe `risk_status_df`
</command_description>
<import_learner_code>
""",
            stderr="""Traceback (most recent call last):
  File "/home/raymond/umuzi/automarker_stuff/data_wrangling/Tilde/automarker_2/gitignore/247-python-perfect/functional_tests/adapter/get_column_names.py", line 30, in <module>
    notebook_module = importlib.import_module(f"{notebook_name}")
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1004, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'data_wrangling'

         """,
        )

        with self.assertRaises(Exception) as context:
            runner.assert_import_learner_code_present()

        self.assertTrue(
            "There was an error importing your code. Please make sure you've named everything correctly. Here is the error message: `ModuleNotFoundError: No module named 'data_wrangling'"
            in str(context.exception)
        )
