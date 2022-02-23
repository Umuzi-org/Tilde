import { resolve } from "path";
import { STATUS_OK, STATUS_ERROR } from "../../consts.mjs";
import shell from "shelljs";

export async function markProjectBase({
  fullPerfectProjectPath,
  fullClonePath,
  lookForTestProblems,
  markerName,
}) {
  const reviewScriptAllOutput = await runMarkerScript({
    markerScriptPath: resolve(`./lib/markers/${markerName}/mark-code.sh`),
    referencePRojectPath: fullPerfectProjectPath,
    fullClonePath,
  });

  const reviewStdOutput = reviewScriptAllOutput.stdout;

  const miscErrors = getTagInnerText(reviewStdOutput, "error");
  if (miscErrors.length > 0) {
    return {
      status: STATUS_ERROR,
      message: "There is something wrong with your code",
      errors: miscErrors,
    };
  }

  const theirTestOutput = getTagInnerText(reviewStdOutput, "their-tests");

  const theirErrors = lookForTestProblems(theirTestOutput);

  if (theirErrors.length > 0) {
    return {
      status: STATUS_ERROR,
      message: "There is something wrong with your tests",
      errors: theirErrors,
    };
  }

  const ourTestOutput = getTagInnerText(reviewStdOutput, "our-tests");
  const ourErrors = lookForTestProblems(ourTestOutput);

  if (ourErrors.length > 0) {
    return {
      status: STATUS_ERROR,
      message: "There is something wrong with your code",
      errors: ourErrors,
    };
  }

  return {
    status: STATUS_OK,
    message: "Looking good! All our automated tests passed",
  };
}

async function runMarkerScript({
  markerScriptPath,
  referencePRojectPath,
  fullClonePath,
}) {
  const markCommand = `CLONE_PATH=${fullClonePath}  REFERENCE_PROJECT_PATH=${referencePRojectPath} /bin/sh -c '${markerScriptPath}'`;

  const reviewOutput = await shell.exec(markCommand);

  if (reviewOutput.stderr.indexOf(`${markerScriptPath}: not found`) !== -1) {
    throw new Error(`${markerScriptPath} NOT FOUND :/`);
  }

  if (
    reviewOutput.stderr.indexOf(`${markerScriptPath}: Permission denied`) !== -1
  ) {
    throw new Error(`${markerScriptPath} Permission denied :/`);
  }

  return reviewOutput;
}

function getTagInnerText(text, tagName) {
  const openTag = `<${tagName}>`;
  const closeTag = `</${tagName}>`;

  if (text.indexOf(openTag) == -1) return "";

  return text.slice(
    text.indexOf(openTag) + openTag.length,
    text.indexOf(closeTag)
  );
}
