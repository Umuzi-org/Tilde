import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK } from "../../consts.mjs";

export default class DoNpmInstall extends Action {
  name = "npm install";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/javascript/do-npm-install-jasmine.sh";
    const command = `DESTINATION_PATH=${destinationPath} /bin/bash -c ${scriptPath}`;

    await shell.exec(command);

    return {
      status: STATUS_OK,
    };
  };
}
