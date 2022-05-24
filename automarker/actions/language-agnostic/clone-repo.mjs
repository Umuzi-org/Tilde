import shell from "shelljs";
import { CLONE_PATH } from "../../env.mjs";
import { STATUS_OK, STATUS_FAIL, STATUS_ERROR } from "../../consts.mjs";
import { Action } from "../index.mjs";
export default class Clone extends Action {
  name = "clone";

  testAction = async function ({ perfectProjectPath, destinationPath }) {
    const clonerScriptPath = "./actions/language-agnostic/copy_dir.sh";

    const cloneCommand = `CLONE_PATH=${CLONE_PATH} DESTINATION_PATH=${destinationPath} PERFECT_PROJECT_PATH=${perfectProjectPath} /bin/bash -c '${clonerScriptPath}'`;

    const stderr = await shell.exec(cloneCommand).stderr;
    if (stderr.match(/No such file or directory/)) {
      return {
        status: STATUS_ERROR,
        message: `Error copying project directory:\n${stderr}`,
      };
    }

    return {
      status: STATUS_OK,
    };
  };

  action = async function ({ repoUrl, destinationPath }) {
    const clonerScriptPath = "./lib/cloner.sh";

    const cloneCommand = `CLONE_PATH=${CLONE_PATH} FULL_CLONE_PATH=${destinationPath} REPO_URL=${repoUrl}  /bin/bash -c '${clonerScriptPath}'`;

    const cloneOutput = await shell.exec(cloneCommand);

    if (cloneOutput.stderr.indexOf("Repository not found.") !== -1) {
      return {
        status: STATUS_ERROR,
        message:
          "Please check that your repo URL is valid and that it is public",
      };
    }

    return {
      status: STATUS_OK,
    };
  };
}
