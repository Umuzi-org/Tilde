import { markProjectBase } from "../utils.mjs";
import { lookForTestProblems } from "../pythonPytest/index.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "pythonPytestOnlyOurTests",
    skipTheirTests: true,
  });
}
