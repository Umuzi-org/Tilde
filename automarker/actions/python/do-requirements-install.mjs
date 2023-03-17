import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_ERROR, STATUS_FAIL } from "../../consts.mjs";

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

    const scriptPath = "./actions/python/do-requirements-install.sh";
    const command = `DESTINATION_PATH=${destinationPath} REQUIREMENTS_DIRECTORY=${requirementsDirectory} /bin/bash -c ${scriptPath}`;
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

    if (scriptErrorOutput.length) {
      return { status: STATUS_ERROR, message: scriptErrorOutput };
    }
    return {
      status: STATUS_OK,
    };
  };
}
