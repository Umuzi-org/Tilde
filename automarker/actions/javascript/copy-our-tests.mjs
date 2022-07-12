import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK } from "../../consts.mjs";

export default class CopyOurTests extends Action {
  name = "copy our tests";
  action = async function ({ perfectProjectPath, destinationPath }) {
    const scriptPath = "./actions/javascript/copy-our-tests.sh";
    const command = `DESTINATION_PATH=${destinationPath} PERFECT_PROJECT_PATH=${perfectProjectPath} ${scriptPath}`;
    await shell.exec(command);

    return {
      status: STATUS_OK,
    };
  };
}
