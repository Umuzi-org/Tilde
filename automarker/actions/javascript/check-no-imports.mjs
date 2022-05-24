import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class CheckNoImports extends Action {
  name = "checking for import statements";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/javascript/check-no-imports.sh";
    const command = `DESTINATION_PATH=${destinationPath} /bin/bash -c ${scriptPath}`;

    const output = await shell.exec(command).stdout;
    console.log("-----------------");
    console.log(output);
    console.log("-----------------");
    TODO;
    //grep -r './' -e 'import'
    return {
      status: STATUS_OK,
    };
  };
}
