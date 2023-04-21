import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";
import { Action } from "../index.mjs";
import shell from "shelljs";

export default class LookForGradleBuildErrors extends Action {
  name = "gradle build";

  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/java/look-for-gradle-build-errors.sh";

    const command = `DESTINATION_PATH=${destinationPath} bash -c ${scriptPath}`;

    const scriptOutput = await shell.exec(command);
    const problems = lookForTestProblems(
      scriptOutput.stdout,
      scriptOutput.stderr
    );

    // console.log({ problems });

    if (problems.length) {
      return {
        status: STATUS_FAIL,
        message: "Your code wont wont run",
        errors: [
          "Your code is so broken that it wont run at all. Don't hand code in if you can't run it",
          ...problems,
        ],
      };
    } else {
      return {
        status: STATUS_OK,
      };
    }
  };
}

function lookForTestProblems(standardOut, standardErr) {
  if (standardOut.match("BUILD SUCCESSFUL")) return [];

  const buildErrors = [
    ...standardErr.matchAll(/.*(\/.*java:\d*: error:.*\n)/g),
  ].map((match) => match[1]);

  if (buildErrors.length) return buildErrors;

  throw new Error(`Unhandled build error:\n\n ${standardErr}`);
}
