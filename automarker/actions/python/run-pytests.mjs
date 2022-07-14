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

    console.log({ problems });

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
  //E   ModuleNotFoundError: No module named 'task1'
  // E   ImportError: cannot import name 'task1' from 'task1' (/home/sheena/workspace/acn-automarker-config/projects/coding_aptitude_mini_course/task1_python/task1.py)
  const lines = testOutput.split("\n");

  const problems = [];

  for (let line of lines) {
    if (line.search("ModuleNotFoundError: No module named") !== -1)
      problems.push(`${line}. Are you sure you named your files correctly?`);

    if (line.search("ImportError: cannot import name") !== -1)
      problems.push(
        `${
          line.split("(")[0]
        }. Are you sure you named everything according to the instructions?`
      );
  }

  if (problems.length > 0) return problems;

  if (testOutput.indexOf("ERRORS") != -1) {
    console.log({ testOutput });
    throw new Error("wtf");
  }

  if (testOutput.indexOf("FAILED") != -1) {
    const stripped = testOutput
      .split("=== short test summary info =====")[0]
      .split("=== FAILURES ===")[1];
    const lines = stripped.split("\n");
    lines.pop();
    lines.shift();

    return lines.map((line) => {
      if (line.indexOf("AssertionError:") === -1)
        throw new Error(`Unknown error type:\n${line}`);

      return line.split("AssertionError: ")[1];
    });
  }
  return [];
}
