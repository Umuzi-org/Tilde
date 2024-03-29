import shell from "shelljs";
import { CLONE_PATH } from "../../env.mjs";
import { STATUS_OK, STATUS_ERROR, STATUS_FAIL } from "../../consts.mjs";
import { Action } from "../index.mjs";
import fs from "fs";
import { join } from "path";

export default class SavePage extends Action {
  name = "fetching page";

  testAction = async function ({
    perfectProjectPath,
    destinationPath,
    // repoUrl,
  }) {
    const clonerScriptPath = "./actions/language-agnostic/copy_dir.sh";

    const cloneCommand = `CLONE_PATH=${CLONE_PATH} DESTINATION_PATH=${destinationPath} PERFECT_PROJECT_PATH=${perfectProjectPath} bash -c '${clonerScriptPath}'`;

    const stderr = await shell.exec(cloneCommand).stderr;
    if (stderr.match(/No such file or directory/)) {
      return {
        status: STATUS_ERROR,
        message: `Error copying project directory:\n${stderr}`,
      };
    }

    return {
      status: STATUS_OK,
    };
  };

  backoff_fetch = async function (url) {
    let tries = 0;

    while (true) {
      try {
        return await fetch(url);
      } catch (error) {
        tries += 1;
        console.log("error fetching", error);
        if (tries > 5) throw error;

        await new Promise((r) => setTimeout(r, 1000 * tries));
      }
    }
  };

  action = async function ({ repoUrl, destinationPath }) {
    const response = await this.backoff_fetch(repoUrl);

    if (response.status == 404) {
      return {
        status: STATUS_FAIL,
        message: `Could not fetch page \`${repoUrl}\`. Response status ${response.status}. Please make sure your url is correct and that your page is public.`,
        errors: [
          `Could not fetch page \`${repoUrl}\`. Response status ${response.status}. Please make sure your url is correct and that your page is public. A 404 error means that the page does not exist.`,
        ],
      };
    }
    if (response.status !== 200) {
      return {
        status: STATUS_ERROR,
        message: `Could not fetch page ${repoUrl}. Response status ${response.status}`,
      };
    }

    const textPromise = response.text();

    if (fs.existsSync(destinationPath)) {
      console.log("directory already exists, deleting");
      fs.rmSync(destinationPath, { recursive: true, force: true });
    }

    fs.mkdirSync(destinationPath, { recursive: true });

    const text = await textPromise;

    fs.writeFileSync(join(destinationPath, "index.html"), text);

    return {
      status: STATUS_OK,
    };
  };
}
