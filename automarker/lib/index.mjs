import { dirNameFromRepoUrl } from "./utils.mjs";
import { CLONE_PATH } from "../env.mjs";
import { STATUS_ERROR, STATUS_OK } from "../consts.mjs";
import shell from "shelljs";

export async function clone({ repoUrl }) {
  const dirName = dirNameFromRepoUrl({ repoUrl });
  const clonerScriptPath = "./lib/cloner.sh";

  const cloneCommand = `CLONE_PATH=${CLONE_PATH} DIR_NAME=${dirName} REPO_URL=${repoUrl} /bin/sh -c '${clonerScriptPath}'`;

  const cloneOutput = await shell.exec(cloneCommand);

  if (cloneOutput.stderr.indexOf("Repository not found.") !== -1) {
    return {
      status: STATUS_ERROR,
      message: "Please check that your repo URL is valid and that it is public",
    };
  }

  return {
    status: STATUS_OK,
  };
}
