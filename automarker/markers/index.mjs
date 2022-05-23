import Clone from "../actions/language-agnostic/clone-repo.mjs";
import { STATUS_ERROR, STATUS_OK } from "../consts.mjs";
import { join, basename } from "path";
import { CLONE_PATH, CONFIGURATION_REPO_PATH } from "../env.mjs";

class Step {
  constructor({ name, Action }) {
    this.name = name;
    this.Action = Action;
  }
}

class Marker {
  mark({ perfectProjectPath, repoUrl, test }) {
    const fullPerfectProjectPath = join(
      CONFIGURATION_REPO_PATH,
      perfectProjectPath
    );

    const destinationPath = test
      ? join(CLONE_PATH, basename(perfectProjectPath))
      : clonePathFromRepoUrl({ repoUrl });

    for (let step of this.steps) {
      const action = new step.Action();
      const result = action.execute({
        test,
        perfectProjectPath: fullPerfectProjectPath,
        destinationPath,
        repoUrl,
      });

      if (result.status === STATUS_ERROR) {
        return {
          status: STATUS_ERROR,
          actionName: step.name || action.name,
          result,
        };
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
    // new Step({ Action: CheckNodeModulesMissing }),
    // new Step({ Action: CheckPackageJsonExists }),
    // new Step({ Action: DoNpmInstall }),
    // new Step({ Action: CheckNodeModulesPresent }),
    // new Step({ Action: CopyTestRunner }),
    // new Step({ Action: RunJasmineTests, name: "running your tests" }),
    // new Step({ Action: CopyOurTests }),
    // new Step({ Action: RunJasmineTests, name: "running our tests" }),
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
