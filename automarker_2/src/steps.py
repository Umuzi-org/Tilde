import os
from pathlib import Path

from exceptions import SystemError, NotYetCompetentError, RedFlagError
import json
from test_runner import TestRunner
from utils import subprocess_run


def get_all_file_paths(directory):
    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(path, filename)


class Step:
    name = "name not defined"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


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
        test_path = Path(config.__file__).parent.parent / "functional_tests"
        final_test_path = clone_dir_path / "functional_tests"

        os.system(f"cp -r {test_path} {clone_dir_path}")

        adapter_path = Path(config.__file__).parent / "adapter"
        os.system(f"cp -r {adapter_path} {final_test_path}")

        assert final_test_path.exists()
        assert (final_test_path / "adapter").exists()


class RunFunctionalTests(Step):
    name = "running functional tests"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        test_path = clone_dir_path / "functional_tests"

        runner = TestRunner(test_path)
        runner.run_tests(fail_fast)

        print("Errors")
        print(json.dumps(runner.results, sort_keys=True, indent=4))

        breakpoint()
        woo


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
            raise RedFlagError(
                f"Your code does not compile at all! This is VERY BAD because it means you handed in code that you couldn't run yourself. Please fix the errors and try again. Here is the error message we got when trying to compile your code:\n\n```\n{stderr}\n```",
                project_uri=project_uri,
                clone_dir_path=clone_dir_path,
                self_test=self_test,
                config=config.__file__,
            )


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
                    raise NotYetCompetentError(
                        error_message,
                        project_uri=project_uri,
                        clone_dir_path=clone_dir_path,
                        self_test=self_test,
                        config=config.__file__,
                    )


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
            raise NotYetCompetentError(
                "It looks like you have submitted your node_modules directory. Please learn about gitignore best practices.",
                project_uri=project_uri,
                clone_dir_path=clone_dir_path,
                self_test=self_test,
                config=config.__file__,
            )


class JavaScriptCheckPackageJsonExists(Step):
    name = "check package.json exists"


class JavaScriptCheckJasmineDevDependency(Step):
    name = "check jasmine dev dependency"


class JavaScriptDoNpmInstall(Step):
    name = "do npm install"


class PythonCheckGitignore(Step):
    name = "check __pycache__ and .pytest_cache__ are not in repo"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        cache_paths = [
            s
            for s in get_all_file_paths(clone_dir_path)
            if ("__pycache__" in s) or (".pytest_cache" in s)
        ]
        if cache_paths:
            raise NotYetCompetentError(
                "It looks like you have submitted some automatically generated files. Please learn about gitignore best practices. Chances are that you are seeing this because of a __pycache__ or .pytest_cache directory",
                project_uri=project_uri,
                clone_dir_path=clone_dir_path,
                self_test=self_test,
                config=config.__file__,
            )


class JavaCheckGitignore(Step):
    name = "check .class files are not in repo"

    def run(self, project_uri, clone_dir_path, self_test, config, fail_fast):
        class_paths = [
            s for s in get_all_file_paths(clone_dir_path) if s.endswith(".class")
        ]
        if class_paths:
            raise NotYetCompetentError(
                "It looks like you have submitted some automatically generated files. Please learn about gitignore best practices. Chances are that you are seeing this because of some .class files in your repo",
                project_uri=project_uri,
                clone_dir_path=clone_dir_path,
                self_test=self_test,
                config=config.__file__,
            )


class PythonCheckRequirementsTxtExists(Step):
    name = "check requirements.txt exists"


class PythonCheckPytestInRequirements(Step):
    name = "check pytest in requirements.txt"


class PythonCreateVirtualEnv(Step):
    name = "create virtual env"


class PythonDoRequirementsInstall(Step):
    name = "do requirements install"


class PythonRunPytests(Step):
    name = "run pytests"
