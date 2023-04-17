import { Action } from "../index.mjs";
import shell from "shelljs";
import { STATUS_OK } from "../../consts.mjs";

export default class CopyOurTests extends Action {
  name = "copying in our tests";
  action = async function ({ perfectProjectPath, destinationPath }) {
    const scriptPath = "./actions/python/copy-our-tests.sh";
    const command = `DESTINATION_PATH=${destinationPath} PERFECT_PROJECT_PATH=${perfectProjectPath} bash -c ${scriptPath}`;
    await shell.exec(command);

    return {
      status: STATUS_OK,
    };
  };
}
