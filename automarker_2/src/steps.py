import os
from pathlib import Path

from exceptions import SystemError
import json
from test_runner import TestRunner


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
        functional_tests/
            adapter/
                adapter.py  # this will allow you to call the learner code like a python function
            test_*.py # these are the tests

    """

    name = "preparation"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_path = Path(config.__file__).parent.parent / "functional_tests"
        os.system(f"cp -r {test_path} {clone_dir_path}")

        adapter_path = Path(config.__file__).parent / "adapter"
        os.system(f"cp -r {adapter_path} {clone_dir_path/'functional_tests'}")


class RunFunctionalTests:
    name = "running functional tests"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_path = clone_dir_path / "functional_tests"

        runner = TestRunner(test_path)
        runner.run_tests(fail_fast)

        print("Errors")
        print(json.dumps(runner.results, sort_keys=True, indent=4))
        print("TODO")


class GradleBuild:
    name = "gradle build"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        os.system(f"cd {clone_dir_path} && ./gradlew build")
