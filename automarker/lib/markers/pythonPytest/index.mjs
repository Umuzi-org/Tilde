import { runMarkerScript, getTagInnerText } from "../../utils.mjs";
import { resolve } from "path";
import { STATUS_OK, STATUS_ERROR } from "../../../consts.mjs";

export async function markProject({ fullPerfectProjectPath, fullClonePath }) {
  const reviewScriptAllOutput = await runMarkerScript({
    markerScriptPath: resolve("./lib/markers/pythonPytest/mark-code.sh"),
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

  const theirErrors = lookForPytestTestProblems(theirTestOutput);

  if (theirErrors.length > 0) {
    return {
      status: STATUS_ERROR,
      message: "There is something wrong with your tests",
      errors: theirErrors,
    };
  }

  const ourTestOutput = getTagInnerText(reviewStdOutput, "our-tests");
  const ourErrors = lookForPytestTestProblems(ourTestOutput);

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

function lookForPytestTestProblems(testOutput) {
  if (testOutput.indexOf("ERRORS") != -1) {
    return [testOutput];
  }
  return [];
}
