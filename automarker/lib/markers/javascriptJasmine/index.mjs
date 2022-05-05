import { markProjectBase } from "../utils.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "javascriptJasmine",
  });
}

function lookForTestProblems(testOutput) {
  if (testOutput.indexOf("jasmine: command not found") != -1) {
    console.error("jasmine: command not found");
    return ["jasmine: command not found"];
  }

  const specCount = (testOutput.match(/SPEC: /g) || []).length;

  if (specCount === 0) {
    return ["No specs found. Are you sure you called jasmine init?"];
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
