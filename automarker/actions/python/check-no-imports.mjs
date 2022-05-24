import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK } from "../../consts.mjs";

export default class CheckNoImports extends Action {
  name = "checking for import statements";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/python/check-no-imports.sh";
    const command = `DESTINATION_PATH=${destinationPath} /bin/bash -c ${scriptPath}`;

    await shell.exec(command);
    TODO;
    //grep -r './' -e 'import'
    return {
      status: STATUS_OK,
    };
  };
}
