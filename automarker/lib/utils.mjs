import { CLONE_PATH } from "../env.mjs";
import { join } from "path";
import shell from "shelljs";

export function dirNameFromRepoUrl({ repoUrl }) {
  const matches = repoUrl.match(/(?<=git@github.com:).*(?=.git)/);
  console.assert(matches.length === 1);
  return matches[0].replace("/", "-");
}

export function clonePathFromRepoUrl({ repoUrl }) {
  return join(CLONE_PATH, dirNameFromRepoUrl({ repoUrl }));
}

export async function runMarkerScript({
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

  //   console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
  //   console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
  //   console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
  //   console.log(reviewOutput.stdout);
  //   console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");

  return reviewOutput.stdout;
}
