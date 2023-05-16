import { STATUS_ERROR, STATUS_OK, STATUS_FAIL } from "../consts.mjs";
import { join, basename, resolve } from "path";
import { CLONE_PATH, CONFIGURATION_REPO_PATH } from "../env.mjs";
import TearDown from "../actions/language-agnostic/tear-down.mjs";

export function dirNameFromRepoUrl({ repoUrl }) {
  const repoMatches = repoUrl.match(/(?<=git@github.com:).*(?=.git)/);
  if (repoMatches !== null) {
    console.assert(repoMatches.length === 1);
    return repoMatches[0].replace("/", "-");
  }
  return repoUrl
    .replace("https://", "")
    .replace("http://", "")
    .replaceAll("/", "-");
}

export function clonePathFromRepoUrl({ repoUrl }) {
  return join(CLONE_PATH, dirNameFromRepoUrl({ repoUrl }));
}

export class Step {
  constructor({ name, Action, actionArgs }) {
    this.name = name;
    this.Action = Action;
    this.actionArgs = actionArgs || {};
  }

  getActionName() {
    return this.name || this.Action.name;
  }

  async execute({ perfectProjectPath, repoUrl, test }) {
    const fullPerfectProjectPath = join(
      CONFIGURATION_REPO_PATH,
      perfectProjectPath
    );
    const destinationPath = test
      ? join(CLONE_PATH, basename(perfectProjectPath))
      : clonePathFromRepoUrl({ repoUrl });

    const action = new this.Action();
    // const actionName = this.name || action.name;
    console.log(`\n--- ACTION: ${this.getActionName()} --- \n`);

    const result = await action.execute({
      test,
      perfectProjectPath: resolve(fullPerfectProjectPath),
      destinationPath: resolve(destinationPath),
      repoUrl,
      ...this.actionArgs,
    });

    return result;
  }
}

export class Marker {
  finalSteps = [
    // new Step({
    //   Action: TearDown,
    // }),
  ];

  async mark({ perfectProjectPath, repoUrl, test }) {
    const result = await this.getMarkResult({
      perfectProjectPath,
      repoUrl,
      test,
    });
    for (let step of this.finalSteps) {
      await step.execute({ perfectProjectPath, repoUrl, test });
    }
    return result;
  }

  async getMarkResult({ perfectProjectPath, repoUrl, test }) {
    console.log({
      CONFIGURATION_REPO_PATH,
      perfectProjectPath,
    });

    for (let step of this.steps) {
      const result = await step.execute({ perfectProjectPath, repoUrl, test });

      const actionName = step.getActionName();

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
