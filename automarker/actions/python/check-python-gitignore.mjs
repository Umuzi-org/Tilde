import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_FAIL, STATUS_OK } from "../../consts.mjs";

export default class CheckPythonGitignore extends Action {
  name = "checking that you didn't submit auto-generated files";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/python/check-python-gitignore.sh";
    const command = `DESTINATION_PATH=${destinationPath} bash -c ${scriptPath}`;

    const output = await shell.exec(command);
    if (output.stdout.trim().length) {
      return {
        status: STATUS_FAIL,
        message:
          "It looks like you have submitted some automatically generated files. Please learn about gitignore best practices. Chances are that you are seeing this because of a __pycache__ or .pytest_cache directory",
      };
    }

    return {
      status: STATUS_OK,
    };
  };
}
