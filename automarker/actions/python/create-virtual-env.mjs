import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_ERROR } from "../../consts.mjs";

export default class CreateVirtualEnv extends Action {
  name = "creating a virtual env";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/python/create-virtual-env.sh";
    const command = `DESTINATION_PATH=${destinationPath} /bin/bash -c ${scriptPath}`;
    const scriptErrorOutput = await shell.exec(command).stderr.trim();

    if (scriptErrorOutput.length) {
      return { status: STATUS_ERROR, message: scriptErrorOutput };
    }
    return {
      status: STATUS_OK,
    };
  };
}
