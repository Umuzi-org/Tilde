import { markProjectBase } from "../utils.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "javaJunit5",
  });
}

export function lookForTestProblems(testOutput) {
  if (testOutput.indexOf("> Task :test FAILED") != -1) return [testOutput];

  if (testOutput.indexOf("> Task :test") == -1)
    return [
      "Tests aren't running. Expected to see '>Task :test but didn't'",
      testOutput,
    ];

  if (testOutput.indexOf(") PASSED") == -1)
    return [
      "No tests are running as far as we can tell. Make sure you have JUnit5 set up properly",
      testOutput,
    ];

  if (testOutput.indexOf("BUILD SUCCESSFUL") != "-1") return [];

  return ["Something went wrong", testOutput];
}
