import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class CheckNoImports extends Action {
  name = "checking for import statements";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/java/check-no-imports.sh";
    const command = `DESTINATION_PATH=${destinationPath} bash -c ${scriptPath}`;

    const output = await shell.exec(command).stdout;
    if (output.length) {
      return {
        status: STATUS_FAIL,
        message:
          "You are using import statements in your code. For this project you shouldn't be importing anything",
      };
    }

    return {
      status: STATUS_OK,
    };
  };
}
