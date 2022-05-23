import { STATUS_ERROR, STATUS_OK } from "../consts.mjs";
import { join, basename } from "path";
import { CLONE_PATH, CONFIGURATION_REPO_PATH } from "../env.mjs";

import Clone from "../actions/language-agnostic/clone-repo.mjs";

import CheckNodeModulesMissing from "../actions/javascript/check-node-modules-missing.mjs";
import CheckPackageJsonExists from "../actions/javascript/check-package-json-exists.mjs";
import CheckJasmineDevDependency from "../actions/javascript/check-jasmine-dev-dependency.mjs";
import DoNpmInstall from "../actions/javascript/do-npm-install.mjs";
import CopyJasmineTestRunner from "../actions/javascript/copy-jasmine-test-runner.mjs";
import CopyOurTests from "../actions/javascript/copy-our-tests.mjs";
import RunJasmineTests from "../actions/javascript/run-jasmine-tests.mjs";
import DoNpmInstallJasmine from "../actions/javascript/do-npm-install-jasmine.mjs";

class Step {
  constructor({ name, Action }) {
    this.name = name;
    this.Action = Action;
  }
}

class Marker {
  async mark({ perfectProjectPath, repoUrl, test }) {
    const fullPerfectProjectPath = join(
      CONFIGURATION_REPO_PATH,
      perfectProjectPath
    );

    const destinationPath = test
      ? join(CLONE_PATH, basename(perfectProjectPath))
      : clonePathFromRepoUrl({ repoUrl });

    for (let step of this.steps) {
      const action = new step.Action();
      const result = await action.execute({
        test,
        perfectProjectPath: fullPerfectProjectPath,
        destinationPath,
        repoUrl,
      });
      const actionName = step.name || action.name;

      if (result === undefined) {
        console.log(result);
        throw new Error(`broken step: ${actionName}: result is undefined`);
      }

      if (result.status === STATUS_ERROR) {
        return {
          status: STATUS_ERROR,
          actionName: actionName,
          result,
        };
      }

      if (result.status !== STATUS_OK) {
        console.log(result);
        throw new Error(`broken step: ${actionName}`);
      }
    }

    // Nothing went wrong. So it must have gone right
    return {
      status: STATUS_OK,
    };
  }
}

export class JavascriptJasmine extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckNodeModulesMissing }),
    new Step({ Action: CheckPackageJsonExists }),
    new Step({ Action: CheckJasmineDevDependency }),
    new Step({ Action: DoNpmInstall }),
    new Step({ Action: CopyJasmineTestRunner }),
    new Step({ Action: RunJasmineTests, name: "running your tests" }),
    new Step({ Action: CopyOurTests }),
    new Step({ Action: RunJasmineTests, name: "running our tests" }),
  ];
}

export class JavascriptJasmineOnlyOurTests extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckNodeModulesMissing }),
    new Step({ Action: DoNpmInstall }),
    new Step({ Action: DoNpmInstallJasmine }),
    new Step({ Action: CopyJasmineTestRunner }),
    new Step({ Action: CopyOurTests }),
    new Step({ Action: RunJasmineTests, name: "running our tests" }),
  ];
}

export function dirNameFromRepoUrl({ repoUrl }) {
  const matches = repoUrl.match(/(?<=git@github.com:).*(?=.git)/);
  console.assert(matches.length === 1);
  return matches[0].replace("/", "-");
}

export function clonePathFromRepoUrl({ repoUrl }) {
  return join(CLONE_PATH, dirNameFromRepoUrl({ repoUrl }));
}
