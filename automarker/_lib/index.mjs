import { clonePathFromRepoUrl } from "./utils.mjs";
import { CONFIGURATION_REPO_PATH, CLONE_PATH } from "../env.mjs";
import { STATUS_ERROR, STATUS_OK } from "../consts.mjs";
import { markers } from "./markers/index.mjs";
import shell from "shelljs";

import { join } from "path";

// export async function clone({ repoUrl }) {
//   //   const dirName = dirNameFromRepoUrl({ repoUrl });
//   const clonerScriptPath = "./lib/cloner.sh";

//   const fullClonePath = clonePathFromRepoUrl({ repoUrl });

//   const cloneCommand = `CLONE_PATH=${CLONE_PATH} FULL_CLONE_PATH=${fullClonePath} REPO_URL=${repoUrl} /bin/sh -c '${clonerScriptPath}'`;

//   const cloneOutput = await shell.exec(cloneCommand);

//   if (cloneOutput.stderr.indexOf("Repository not found.") !== -1) {
//     return {
//       status: STATUS_ERROR,
//       message: "Please check that your repo URL is valid and that it is public",
//     };
//   }

//   return {
//     status: STATUS_OK,
//   };
// }

// export function getProjectConfig({ contentItemId, flavours }) {
//   const configFilePath = `${CONFIGURATION_REPO_PATH}/config.yaml`;
//   const allConfig = yaml.load(fs.readFileSync(configFilePath, "utf8"));

//   const matchingConfig = allConfig
//     .filter((o) => o.contentItemId === contentItemId)
//     .filter((o) => arraysEqual(o.flavours, flavours));

//   if (matchingConfig.length === 1) return matchingConfig[0];
// }

export async function mark({ config, repoUrl }) {
  const markProject = markers[config.marker];
  if (markProject === undefined)
    return {
      status: STATUS_ERROR,
      message: `Undefined marker: ${
        config.marker
      }. This probably means that the configuration repo is misconfigured. Available markers are: ${Object.keys(
        markers
      )}. You can find these in: lib/markers/index.mjs`,
    };

  const { perfectProjectPath } = config;
  const fullPerfectProjectPath = join(
    CONFIGURATION_REPO_PATH,
    perfectProjectPath
  );

  const fullClonePath = clonePathFromRepoUrl({ repoUrl });

  return await markProject({ fullPerfectProjectPath, fullClonePath });
}