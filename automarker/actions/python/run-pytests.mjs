import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class RunPytests extends Action {
  name = "running pytest";
  action = async function ({ destinationPath }) {
    const scriptPath = "actions/python/run-pytests.sh";
    const command = `DESTINATION_PATH=${destinationPath} /bin/bash -c ${scriptPath}`;

    const scriptOutput = await shell.exec(command);
    const problems = lookForTestProblems(
      scriptOutput.stdout,
      scriptOutput.stderr
    );

    if (problems.length) {
      return {
        status: STATUS_FAIL,
        message: "Pytest errors",
        errors: problems,
      };
    } else {
      return {
        status: STATUS_OK,
      };
    }
  };
}

function lookForTestProblems(testOutput) {
  if (testOutput.indexOf("ERRORS") != -1) {
    return [testOutput];
  }
  if (testOutput.indexOf("FAILURES") != -1) {
    return [testOutput];
  }
  return [];
}
