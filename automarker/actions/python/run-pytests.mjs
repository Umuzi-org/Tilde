import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class RunPytests extends Action {
  name = "running pytest";
  action = async function ({ destinationPath, repoUrl = "" }) {
    const scriptPath = "actions/python/run-pytests.sh";
    const command = `DESTINATION_PATH=${destinationPath} SUBMISSION_URL=${repoUrl} /bin/bash -c ${scriptPath}`;

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

/*These are things that would stop the tests from running at all, eg the function we are trying to test doesn't exist */
function lookForSeriousErrors(testOutput) {
  // E   ModuleNotFoundError: No module named 'task1'
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
        }. Are you sure you named everything according to the instructions? Make sure all files, functions, and everything are named accurately. If you don't follow the instructions EXACTLY then your code will not pass`
      );
  }

  return problems;
}

function lookForFailures(testOutput) {
  if (testOutput.indexOf("FAILED") === -1) return [];

  const stripped = testOutput
    .split("=== short test summary info =====")[0]
    .split("=== FAILURES ===")[1]
    .split("==== warnings summary ====")[0];

  const lines = stripped.split("\n");
  lines.pop();
  lines.shift();

  return lines.map((line) => {
    if (line.indexOf("TypeError:") !== -1) {
      return `${
        line.split("TypeError: ")[1]
      } - please make sure you are following the instructions. Pay close attention to all names (including file paths) and function arguments`;
    }

    if (line.indexOf("AssertionError:") !== -1) {
      return line.split("AssertionError: ")[1];
    }

    const match = line.match(/(\w*\.py:\d+:.*)/g);
    // eg: line = "/home/sheena/workspace/Tilde/gitignore/automark_clone_path/Umuzi-org-Kopano-Mosai-758-contentitem-python/task6.py:12: UnboundLocalError: local variable 'maximum' referenced before assignment"
    // match  = ["task6.py:12: UnboundLocalError: local variable 'maximum' referenced before assignment"]

    if (match.length === 1) return match[0];

    console.log("==============================");
    console.log("==============================");
    console.log(lines);
    console.log("==============================");
    console.log("==============================");
    throw new Error(`Unknown error type:\n \'\'\'\n\t${line}\n\`\`\``);
  });
}

function lookForWarnings(testOutput) {
  if (testOutput.indexOf("==== warnings summary ====") === -1) return [];

  const stripped = testOutput
    .split("==== warnings summary ====")[1]
    .split("=== short test summary info =====")[0];

  const lines = stripped.split("\n");
  lines.pop();
  lines.shift();

  return lines
    .map((line) => {
      const match = line.match(/(\w*\.py:\d+:.*)/g);
      if (match === null) return;

      if (match.length === 1) {
        const warning = match[0];
        if (warning.match(/DeprecationWarning/)) {
          return `${warning}. If something is deprecated then it means that it is old school. Try to use modern best practices`;
        }
        return warning;
      }
      if (match.length > 1) {
        console.log("==========================");
        console.log("==========================");
        console.log(lines);
        console.log("==========================");
        console.log("==========================");
        throw new Error(`unexpected line format:\n\`\`\`${line}\`\`\``);
      }
    })
    .filter((line) => line !== undefined);
}

function lookForTestProblems(testOutput) {
  const errors = lookForSeriousErrors(testOutput);
  if (errors.length > 0) return errors;

  // Just a sanity check. We should have found all the ERRORs in the last step
  if (testOutput.indexOf("ERRORS") != -1) {
    const lines = testOutput
      .split("==== ERRORS ====")[1]
      .split("=== short test summary info =====")[0]
      .split("\n");

    lines.shift();

    if (lines[0][0] !== "_") {
      console.log({ testOutput });
      throw new Error("wtf");
    }

    lines.shift();
    lines.pop();
    return lines;
  }

  const failures = lookForFailures(testOutput);
  const warnings = lookForWarnings(testOutput);

  return [...failures, ...warnings];
}
