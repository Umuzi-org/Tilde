function dirNameFromRepoUrl({ repoUrl }) {
  return repoUrl
    .slice("https://github.com/".length, -".git".length)
    .replace("/", "--");
}

export async function clone({ repoUrl }) {
  const dirName = dirNameFromRepoUrl({ repoUrl });
  console.log(`cloning to ${dirName}`);
  const clonerScriptPath = "./lib/cloner.sh";

  const cloneCommand = `CLONE_PATH=${clonePath} DIR_NAME=${dirName} REPO_URL=${repoUrl} /bin/sh -c '${clonerScriptPath}'`;

  const cloneOutput = await shell.exec(cloneCommand);

  if (cloneOutput.stdout.indexOf("404 Not Found") !== -1) {
    return {
      status: STATUS_ERROR,
      message: "Please check that your repo URL is valid and that it is public",
    };
  }

  if (cloneOutput.stderr.indexOf(`${clonerScriptPath}: not found`) !== -1) {
    console.error(`${clonerScriptPath} NOT FOUND :/`);

    return {
      status: STATUS_ERROR,
      message: "Internal server Error",
    };
  }

  return {
    status: STATUS_OK,
  };
}
