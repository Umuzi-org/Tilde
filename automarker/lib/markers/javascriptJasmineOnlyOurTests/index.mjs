import { markProjectBase } from "../utils.mjs";
import { lookForTestProblems } from "../javascriptJasmine/index.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "javascriptJasmineOnlyOurTests",
    skipTheirTests: true,
  });
}
