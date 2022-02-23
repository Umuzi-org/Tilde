import { runMarkerScript } from "../../utils.mjs";
import { resolve } from "path";

export async function markProject({ fullPerfectProjectPath, fullClonePath }) {
  const reviewScriptOutput = await runMarkerScript({
    markerScriptPath: resolve("./lib/markers/pythonPytest/mark-code.sh"),
    referencePRojectPath: fullPerfectProjectPath,
    fullClonePath,
  });

  return reviewScriptOutput;
}
