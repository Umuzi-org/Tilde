import { STATUS_ERROR, STATUS_OK, STATUS_FAIL } from "../consts.mjs";
import { join, basename } from "path";
import { CLONE_PATH, CONFIGURATION_REPO_PATH } from "../env.mjs";

export function dirNameFromRepoUrl({ repoUrl }) {
  const matches = repoUrl.match(/(?<=git@github.com:).*(?=.git)/);
  console.assert(matches.length === 1);
  return matches[0].replace("/", "-");
}

export function clonePathFromRepoUrl({ repoUrl }) {
  return join(CLONE_PATH, dirNameFromRepoUrl({ repoUrl }));
}

export class Step {
  constructor({ name, Action }) {
    this.name = name;
    this.Action = Action;
  }
}

export class Marker {
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
      const actionName = step.name || action.name;
      console.log(`\n--- ACTION: ${actionName} --- `);
      const result = await action.execute({
        test,
        perfectProjectPath: fullPerfectProjectPath,
        destinationPath,
        repoUrl,
      });

      if (result === undefined) {
        return {
          status: STATUS_ERROR,
          message: `broken step: ${actionName}: result is undefined`,
        };
      }

      if (result.status === STATUS_FAIL || result.status === STATUS_ERROR) {
        return {
          status: result.status,
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
