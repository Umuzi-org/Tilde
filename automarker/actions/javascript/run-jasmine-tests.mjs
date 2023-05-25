import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";
import { Action } from "../index.mjs";
import shell from "shelljs";

export default class RunJasmineTests extends Action {
  name = "jasmine tests";

  action = async function ({ destinationPath }) {
    const scriptPath = "actions/javascript/run-jasmine-tests.sh";
    const command = `DESTINATION_PATH=${destinationPath} bash -c ${scriptPath}`;

    const scriptOutput = await shell.exec(command);
    const problems = lookForTestProblems(
      scriptOutput.stdout,
      scriptOutput.stderr
    );

    if (problems.length) {
      return {
        status: STATUS_FAIL,
        message: "Jasmine test errors",
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
  if (testOutput.indexOf("jasmine: command not found") != -1) {
    console.error("jasmine: command not found");
    return ["jasmine: command not found"];
  }

  const specCount = (testOutput.match(/SPEC: /g) || []).length;

  if (specCount === 0) {
    return [
      "Something went wrong while running the tests. Are you sure the file and function names are as they should be? Did you remember to `export` all the things you were supposed to? Double check the project instructions to make sure.",
    ];
  }

  const moduleNotFound = testOutput.match(/(Error: Cannot find module .*)\n/);
  if (moduleNotFound) {
    return [moduleNotFound[1]];
  }

  if (testOutput.indexOf("No specs found") !== -1) {
    return ["No specs found. Are you sure you called jasmine init?"];
  }

  return testOutput.match(/SPEC FAILED: .*(?=\n)/g) || [];
}
