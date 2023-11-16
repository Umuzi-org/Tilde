import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_ERROR, STATUS_FAIL } from "../../consts.mjs";
import { join } from "path";
import fs from "fs";
import { stdoutHasErrors } from "./python-utils.mjs";

export default class DoRequirementsInstall extends Action {
  name = "installing requirements.txt";

  action = async function ({
    destinationPath,
    perfectProjectPath,
    useOurs = false,
  }) {
    const requirementsDirectory = useOurs
      ? perfectProjectPath
      : destinationPath;

    const requirementsFilePath = join(
      requirementsDirectory,
      "requirements.txt"
    );

    console.log({
      requirementsDirectory,
      destinationPath,
      perfectProjectPath,
    });

    if (!fs.existsSync(requirementsFilePath)) {
      return {
        status: STATUS_FAIL,
        message:
          "Your requirements.txt file seems to be missing. Please make sure you include all required files.",
      };
    }

    const scriptPath = "./actions/python/do-requirements-install.sh";
    const command = `DESTINATION_PATH=${destinationPath} REQUIREMENTS_DIRECTORY=${requirementsDirectory} bash -c ${scriptPath}`;
    const scriptErrorOutput = await shell.exec(command).stderr.trim();

    if (
      scriptErrorOutput.match(
        /Could not find a version that satisfies the requirement/
      )
    ) {
      return {
        status: STATUS_FAIL,
        message: `It looks like you have an error in your requirements.txt file. Here is the full error message:\n\n${scriptErrorOutput}`,
      };
    }

    if (stdoutHasErrors({ scriptErrorOutput })) {
      return { status: STATUS_ERROR, message: scriptErrorOutput };
    }
    return {
      status: STATUS_OK,
    };
  };
}
