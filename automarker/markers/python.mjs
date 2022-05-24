import { Marker, Step } from "./utils.mjs";

import Clone from "../actions/language-agnostic/clone-repo.mjs";

import CheckRequirementsTxtExists from "../actions/python/check-requirements-txt-exists.mjs";
import CheckPytestInRequirements from "../actions/python/check-pytest-in-requirements.mjs";
import DoRequirementsInstall from "../actions/python/do-requirements-install.mjs";
import CheckPythonGitignore from "../actions/python/check-python-gitignore.mjs";
import CheckNoImports from "../actions/python/check-no-imports.mjs";
import DoInstallPytest from "../actions/python/do-install-pytest.mjs";
import CopyOurPytests from "../actions/python/copy-our-tests.mjs";
import RunPytests from "../actions/python/run-pytests.mjs";
import CreateVirtualEnv from "../actions/python/create-virtual-env.mjs";

export class PythonPytest extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckPythonGitignore }),
    new Step({ Action: CheckRequirementsTxtExists }),
    new Step({ Action: CheckPytestInRequirements }),
    new Step({ Action: CreateVirtualEnv }),
    new Step({ Action: DoRequirementsInstall }),
    new Step({ Action: RunPytests, name: "running your tests" }),
    new Step({ Action: CopyOurPytests }),
    new Step({ Action: RunPytests, name: "running our tests" }),
  ];
}

export class PythonPytestOnlyOurTests extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckPythonGitignore }),
    new Step({ Action: CreateVirtualEnv }),
    new Step({ Action: DoInstallPytest }),
    new Step({ Action: CopyOurPytests }),
    new Step({ Action: RunPytests, name: "running our tests" }),
  ];
}

export class PythonPytestKatas extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckPythonGitignore }),
    new Step({ Action: CheckNoImports }),
    new Step({ Action: CreateVirtualEnv }),
    new Step({ Action: DoInstallPytest }),
    new Step({ Action: CopyOurPytests }),
    new Step({ Action: RunPytests, name: "running our tests" }),
  ];
}
