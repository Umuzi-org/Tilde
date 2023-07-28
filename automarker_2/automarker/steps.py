import os
import datetime
from pathlib import Path
from .exceptions import SystemError
from .automarker_test_runner import (
    PythonTestRunner,
    JavaTestRunner,
    JavaScriptTestRunner,
)
import re
from .utils import subprocess_run
from .constants import (
    STEP_STATUS_WAITING,
    STEP_STATUS_RUNNING,
    STEP_STATUS_ERROR,
    STEP_FINAL_STATUSES,
    STEP_STATUS_PASS,
    STEP_STATUS_NOT_YET_COMPETENT,
    STEP_STATUS_RED_FLAG,
)
import json


def get_all_file_paths(directory):
    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(path, filename)


class Step:
    name = "name not defined"

    class _StopStepException(Exception):
        """raised when the step outcome is set. This prevents the step from continuing to run"""

    def __init__(self):
        self.status = STEP_STATUS_WAITING
        self.message = None
        self.details = None
        self.start_time = None
        self.end_time = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        raise NotImplementedError(f"{self} has not implemented run()")

    def duration(self):
        if self.start_time is None:
            return 0
        return self.end_time - self.start_time

    def details_string(self):
        """Override this in child classes if details is complicated"""
        return self.details

    def execute_run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        self.start_time = datetime.datetime.now()
        self.status = STEP_STATUS_RUNNING

        try:
            self.run(project_uri, clone_dir_path, self_test, config, fail_fast)
        except self._StopStepException:
            pass  # nothing to do. The step terminated normally

        assert (
            self.status in STEP_FINAL_STATUSES
        ), f"{self}: Remember to call set_outcome in your run method"

    def set_outcome(self, status, message=None, details=None):
        assert (
            self.status == STEP_STATUS_RUNNING
        ), f"You can only set the outcome once. It was already set to: \n\tstatus = {self.status} \n\tmessage={self.message}"

        self.status = status
        self.message = message
        self.details = details
        self.end_time = datetime.datetime.now()

        raise self._StopStepException()


class Clone(Step):
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
        self.set_outcome(status=STEP_STATUS_PASS)


class PrepareFunctionalTests(Step):
    """Copy the adapter and tests into the right place so we can run them. The final directory structure will look like:

    clone_dir_path/
        functional_tests/
            adapter/
                adapter.py  # this will allow you to call the learner code like a python function
            test_*.py # these are the tests

    """

    name = "preparing functional tests"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        self._run(project_uri, clone_dir_path, self_test, config, fail_fast)
        self.set_outcome(status=STEP_STATUS_PASS)

    def _run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_paths = []
        adapter_paths = []

        final_test_path = clone_dir_path / "functional_tests"
        os.mkdir(final_test_path)

        if config.include_functional_tests_from:
            for s in config.include_functional_tests_from:
                tests_path = (
                    Path(config.__file__).parent.parent.parent / s
                ).parent / "functional_tests"
                test_paths.append(tests_path)

                adapter_path = (
                    Path(config.__file__).parent.parent.parent / s / "adapter"
                )
                adapter_paths.append(adapter_path)

        test_paths.append(Path(config.__file__).parent.parent / "functional_tests")

        for test_path in test_paths:
            os.system(f"cp -r {test_path} {clone_dir_path}")

        # print(os.listdir(final_test_path))
        # breakpoint()

        adapter_paths.append(Path(config.__file__).parent / "adapter")
        for adapter_path in adapter_paths:
            os.system(f"cp -r {adapter_path} {final_test_path}")

        assert final_test_path.exists()
        adapter_path = final_test_path / "adapter"
        assert adapter_path.exists(), f"{adapter_path} does not exist"


class JavaPrepareFunctionalTests(PrepareFunctionalTests):
    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        self._run(project_uri, clone_dir_path, self_test, config, fail_fast)
        # try to build the tests. If the learner named anything badly then
        # this will fail and we can give them a useful error message
        adapter_dir = clone_dir_path / "functional_tests" / "adapter"
        build_command = f"javac --class-path {clone_dir_path} {adapter_dir/'*.java'}"
        stdout, stderr = subprocess_run(build_command)
        if stderr:
            if "cannot find symbol" in stderr:
                error = (
                    "cannot find symbol"
                    + stderr.split("cannot find symbol")[1].split("location")[0]
                )
                error = "\n".join([s for s in error.split("\n") if s.strip()])
                message = f"There was an error when we tried to use your code. Please make sure you've named everything correctly. Here is the error message: \n{error}"
                self.set_outcome(status=STEP_STATUS_NOT_YET_COMPETENT, message=message)
        else:
            self.set_outcome(status=STEP_STATUS_PASS)


class _RunFunctionalTests(Step):
    name = "running functional tests"

    TestRunnerClass = None  # override this in child classes

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_path = clone_dir_path / "functional_tests"

        runner = self.TestRunnerClass(test_path, clone_dir_path=clone_dir_path)
        runner.run_tests(fail_fast)

        if runner.has_errors():
            message = f"Your code has errors. Please fix them and try again"
            self.set_outcome(
                status=runner.status(),
                message=message,
                details=runner.fail_results(),
            )
            return

        self.set_outcome(status=STEP_STATUS_PASS)

    def details_string(self):
        result = ""
        for test_suit, test_functions in self.details.items():
            result += f"\n\n# Test suite: {test_suit[:-3]}"
            for test_function, test_result in test_functions.items():
                result += f"\n## Test: {test_function}"
                for test_result in test_result:
                    command_description = test_result["command_description"]
                    error_message = test_result["error_message"]
                    result += f"\n### FAILURE: There was an error when we tried to {command_description}:\n{error_message}"
        return result


class PythonRunFunctionalTests(_RunFunctionalTests):
    TestRunnerClass = PythonTestRunner


class JavaRunFunctionalTests(_RunFunctionalTests):
    TestRunnerClass = JavaTestRunner


class JavaScriptRunFunctionalTests(_RunFunctionalTests):
    TestRunnerClass = JavaScriptTestRunner


class GradleBuild(Step):
    name = "gradle build"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        os.system(f"cd {clone_dir_path} && ./gradlew build")
        TODO  # look for errors


class JavaBuild(Step):
    """Does it build? Just use javac"""

    name = "java build"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        command = f"javac {clone_dir_path}/*.java"
        stdout, stderr = subprocess_run(command)
        if len(stderr):
            error = stderr.replace(str(clone_dir_path.resolve()), "").strip()

            message = f"Your code does not compile at all! This is VERY BAD because it means you handed in code that you couldn't run yourself. Please fix the errors and try again. Here is the error message:\n\n{error}"

            self.set_outcome(status=STEP_STATUS_RED_FLAG, message=message)

        self.set_outcome(status=STEP_STATUS_PASS)


class _CheckNoImports(Step):
    file_extension = None
    checks = []

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        assert self.file_extension, "What kinds of files are we looking at here"
        assert self.checks, "What kinds of checks are we doing here?"

        all_paths = [
            s
            for s in get_all_file_paths(clone_dir_path)
            if s.endswith(self.file_extension)
        ]

        for path in all_paths:
            text = Path(path).read_text()
            for check, error_message in self.checks:
                if check(text):
                    self.set_outcome(
                        status=STEP_STATUS_NOT_YET_COMPETENT, message=error_message
                    )

        self.set_outcome(status=STEP_STATUS_PASS)


class JavaCheckNoImports(_CheckNoImports):
    name = "check no imports"

    file_extension = ".java"
    checks = [
        (
            lambda text: "import" in text,
            "You shouldn't need to import anything in this project. Please remove all `import` statements from your code.",
        )
    ]


class PythonCheckNoImports(_CheckNoImports):
    name = "check no imports"
    file_extension = ".py"

    checks = [
        (
            lambda text: "import " in text,
            "You shouldn't need to import anything in this project. Please remove all `import` statements from your code.",
        )
    ]


class JavaScriptCheckNoImports(_CheckNoImports):
    name = "check no imports"
    file_extension = ".js"
    checks = [
        (
            lambda text: "import " in text,
            "You shouldn't need to import anything in this project. Please remove all `import` statements from your code.",
        ),
        (
            lambda text: "require(" in text,
            "You shouldn't need to import anything in this project. Please remove all `require` statements from your code.",
        ),
    ]


class JavaRunJunitJupiterTests(Step):
    name = "run junit jupiter tests"


class JavaScriptCheckNodeModulesMissing(Step):
    name = "check node modules missing"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        node_module_paths = [
            s for s in get_all_file_paths(clone_dir_path) if "node_modules" in s
        ]
        if node_module_paths:
            message = "It looks like you have submitted your node_modules directory. Please learn about gitignore best practices."

            self.set_outcome(STEP_STATUS_NOT_YET_COMPETENT, message=message)

        self.set_outcome(status=STEP_STATUS_PASS)


class JavaScriptCheckPackageJsonExists(Step):
    name = "check package.json exists"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        package_json_path = clone_dir_path / "package.json"
        if package_json_path.exists():
            with open(package_json_path) as f:
                try:
                    json.load(f)
                    self.set_outcome(STEP_STATUS_PASS)

                except json.decoder.JSONDecodeError:
                    message = "It looks like your package.json file is not valid JSON. Do some research about how a package.json file should look and behave. "
                    self.set_outcome(STEP_STATUS_RED_FLAG, message=message)

        else:
            message = (
                "This project requires a package.json file but you did not submit one"
            )

            self.set_outcome(STEP_STATUS_NOT_YET_COMPETENT, message=message)

        self.set_outcome(status=STEP_STATUS_PASS)


class JavaScriptCheckJasmineDevDependency(Step):
    name = "check jasmine dev dependency"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        package_json_path = clone_dir_path / "package.json"
        with open(package_json_path) as f:
            package_json = json.load(f)

        dev_dependencies = package_json.get("devDependencies", {})
        dependencies = package_json.get("dependencies", {})

        if "jasmine" in dependencies:
            self.set_outcome(
                STEP_STATUS_NOT_YET_COMPETENT,
                message="It looks like you installed jasmine as a regular dependency. Please npm install it as a dev dependency instead",
            )
            return

        if "jasmine" not in dev_dependencies:
            self.set_outcome(
                STEP_STATUS_NOT_YET_COMPETENT,
                message="It looks like you have not installed jasmine at all. Please npm install it as a dev dependency",
            )
            return

        test_script = package_json.get("scripts", {}).get("test")
        if "jasmine" not in test_script:
            self.set_outcome(
                STEP_STATUS_NOT_YET_COMPETENT,
                message="We should be able to run your tests using `npm run test`. Please make sure that you have set up a test script in your package.json",
            )
            return

        self.set_outcome(STEP_STATUS_PASS)


class JavaScriptRunLearnerJasmineTests(Step):
    name = "run learner's tests with jasmine"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        stdout, stderr = subprocess_run(f"cd {clone_dir_path} && npm run test")

        if "npm ERR! Missing script:" in stderr:
            self.set_outcome(
                STEP_STATUS_NOT_YET_COMPETENT,
                message="We should be able to run your tests using `npm run test`. Please make sure that you have set up a test script in your package.json",
            )
            return
        if "No specs found" in stdout:
            self.set_outcome(
                STEP_STATUS_RED_FLAG,
                message="It looks like you have not written any tests. Please test your work. Tests save lives (I'm not kidding).",
            )
            return

        if stderr:
            self.set_outcome(
                STEP_STATUS_RED_FLAG,
                message=f"There was an error while running your tests. Please make sure that you submit valid code! If you can't run your tests then neither can we.\n\nHere is the error:\n\n{stderr}",  # todo: sanitise the error. It will contain th clone directory
            )
            return

        counts = re.search(f"(\d+) specs?, (\d+) failures?", stdout)
        if counts:
            specs, fails = counts.groups()
            if int(fails) > 0:
                self.set_outcome(
                    STEP_STATUS_RED_FLAG,
                    message=f"Your tests failed. Please fix them. Here is the output from running your tests:\n\n{stdout}",  # todo: sanitise the error. It will contain th clone directory
                )
                return
            else:
                self.set_outcome(STEP_STATUS_PASS)
                return
        breakpoint()
        shouldnt_be_here


class JavaScriptDoNpmInstall(Step):
    name = "do npm install"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        stdout, stderr = subprocess_run(
            f"cd {clone_dir_path} && npm install --include=dev"
        )
        if len(stderr):
            message = "There was an error while running `npm install`. Please make sure that you submit valid code! if you can't `npm install` your dependencies then neither can we."
            self.set_outcome(status=STEP_STATUS_RED_FLAG, message=message)
        else:
            self.set_outcome(status=STEP_STATUS_PASS)


class PythonCheckGitignore(Step):
    name = "check __pycache__ and .pytest_cache__ are not in repo"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        cache_paths = [
            s
            for s in get_all_file_paths(clone_dir_path)
            if ("__pycache__" in s) or (".pytest_cache" in s)
        ]
        if cache_paths:
            message = "It looks like you have submitted some automatically generated files. Please learn about gitignore best practices. Chances are that you are seeing this because of a __pycache__ or .pytest_cache directory"
            self.set_outcome(status=STEP_STATUS_NOT_YET_COMPETENT, message=message)

        self.set_outcome(status=STEP_STATUS_PASS)


class JavaCheckGitignore(Step):
    name = "check .class files are not in repo"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        class_paths = [
            s for s in get_all_file_paths(clone_dir_path) if s.endswith(".class")
        ]
        if class_paths:
            message = "It looks like you have submitted some automatically generated files. Please learn about gitignore best practices. Chances are that you are seeing this because of some .class files in your repo"
            self.set_outcome(status=STEP_STATUS_NOT_YET_COMPETENT, message=message)

        self.set_outcome(status=STEP_STATUS_PASS)


class PythonCheckPytestInRequirements(Step):
    name = "check pytest in requirements.txt"


class PythonCreateVirtualEnv(Step):
    name = "create virtual env"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        command = f"python3 -m venv {clone_dir_path/'automarker_venv'}"
        stdout, stderr = subprocess_run(command)
        if len(stderr):
            self.set_outcome(STEP_STATUS_ERROR, message=stderr)
        else:
            self.set_outcome(status=STEP_STATUS_PASS)


class PythonDoRequirementsTxtInstall(Step):
    name = "pip install requirements.txt"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        command = f"{clone_dir_path/'automarker_venv'/'bin'/'pip'} install -r {clone_dir_path/'requirements.txt'}"
        stdout, stderr = subprocess_run(command)
        if len(stderr):
            if stderr.startswith("ERROR: Could not open requirements file"):
                self.set_outcome(
                    STEP_STATUS_NOT_YET_COMPETENT,
                    message="It looks like you have not created a requirements.txt file. Please create one.",
                )
            elif stderr.startswith("ERROR: Invalid requirement:"):
                # TODO: mention the broken requirement in the error message
                self.set_outcome(
                    STEP_STATUS_RED_FLAG,
                    message="It looks like you have a typo in your requirements.txt file. Please fix it. Make sure `pip install requirements.txt` works. Don't hand in code that you cannot run yourself!",
                )
            if stderr.startswith(
                "ERROR: Could not find a version that satisfies the requirement"
            ):
                # TODO: mention the broken requirement in the error message
                # eg: "ERROR: Could not find a version that satisfies the requirement lkjhalohiasdijpo ". in this case mention lkjhalohiasdijpo
                self.set_outcome(
                    STEP_STATUS_RED_FLAG,
                    message="Your requirements.txt file is trying to install something that does not exist. Make sure `pip install requirements.txt` works. Don't hand in code that you cannot run yourself!",
                )
            else:
                breakpoint()
                what
        else:
            self.set_outcome(status=STEP_STATUS_PASS)


class PythonRunPytests(Step):
    name = "run pytests"
