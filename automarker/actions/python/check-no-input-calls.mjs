import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class CheckNoInputCalls extends Action {
  name = "checking for calls to input() function";
  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/python/check-no-input-calls.sh";
    const command = `DESTINATION_PATH=${destinationPath} /bin/bash -c ${scriptPath}`;

    const output = await shell.exec(command).stdout;
    if (output.length) {
      return {
        status: STATUS_FAIL,
        message:
          "You are using calls to the input() function in your code. Please remove those. Functions should have perfectly normal function arguments. User input is not required",
      };
    }

    return {
      status: STATUS_OK,
    };
  };
}
