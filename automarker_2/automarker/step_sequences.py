"""
A lot of the time, a marker will have the exact same steps as other markers. 
"""
from . import steps


def python_kata_sequence():
    """This is a very permissive sequence. Learners can submit code that is totally bananas, so long as it works we are happy"""
    return [
        steps.Clone(),
        steps.PythonCheckNoImports(),
        steps.PrepareFunctionalTests(),
        steps.PythonRunFunctionalTests(),
    ]


def javascript_kata_sequence():
    return [
        steps.Clone(),
        steps.JavaScriptCheckNoImports(),
        steps.PrepareFunctionalTests(),
        steps.JavaScriptRunFunctionalTests(),
    ]


def java_kata_sequence():
    return [
        steps.Clone(),
        steps.JavaCheckNoImports(),
        steps.JavaBuild(),
        steps.JavaPrepareFunctionalTests(),
        steps.JavaRunFunctionalTests(),
    ]


python_base = [
    steps.Clone(),
    steps.PythonCheckGitignore(),
]

python_functional_tests = [
    # doesn't run learner tests
    steps.PrepareFunctionalTests(),
    steps.PythonRunFunctionalTests(),
]


def python_sequence(do_pip_install=False, run_learner_pytest=False):
    l = []
    l.extend(python_base)
    if run_learner_pytest:
        assert (
            do_pip_install
        ), "configuration error. If the learner was meant to write pytests then they should install pytest"
        l.extend(
            [
                steps.PythonCheckPytestInRequirements(),
                steps.PythonCreateVirtualEnv(),
                steps.PythonDoRequirementsTxtInstall(),
                steps.PythonRunPytests(),
            ]
        )

    elif do_pip_install:
        assert not run_learner_pytest
        l.extend(
            [
                steps.PythonCreateVirtualEnv(),
                steps.PythonDoRequirementsTxtInstall(),
            ]
        )
    l.extend(python_functional_tests)
    return l


node_base = [
    steps.Clone(),
    steps.JavaScriptCheckNodeModulesMissing(),
]

node_functional_tests = [
    steps.PrepareFunctionalTests(),
    steps.JavaScriptRunFunctionalTests(),
]


def javascript_sequence(do_npm_install=False):
    l = []
    l.extend(node_base)
    if do_npm_install:
        l.extend(
            [steps.JavaScriptCheckPackageJsonExists(), steps.JavaScriptDoNpmInstall()]
        )
    l.extend(node_functional_tests)
    return l


def java_sequence():
    return [
        steps.Clone(),
        steps.JavaCheckGitignore(),
        steps.JavaBuild(),
        steps.JavaPrepareFunctionalTests(),
        steps.JavaRunFunctionalTests(),
    ]


def java_gradle_sequence():
    return [
        steps.Clone(),
        steps.JavaCheckGitignore(),
        steps.GradleBuild(),
        steps.JavaPrepareFunctionalTests(),
        steps.JavaRunFunctionalTests(),
    ]
