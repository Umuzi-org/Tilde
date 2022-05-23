import { markProjectBase } from "../utils.mjs";
import { lookForTestProblems } from "../javaJunit5/index.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "javaJunit5", // we use the same marker script as the javaJunit5 one,
    skipTheirTests: true, // we just dont care about their test output
  });
}
