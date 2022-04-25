import { markProjectBase } from "../utils.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "pythonPytest",
  });
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
