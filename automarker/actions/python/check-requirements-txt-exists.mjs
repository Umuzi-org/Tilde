import { Action } from "../index.mjs";
import fs from "fs";
import { join } from "path";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class CheckRequirementsTxtExists extends Action {
  name = "checking that requirements.txt exists";
  action = async function ({ destinationPath }) {
    const path = join(destinationPath, "requirements.txt");
    if (fs.existsSync(path)) {
      return {
        status: STATUS_OK,
      };
    }

    return {
      status: STATUS_FAIL,
      message:
        "Looks like you didn't include a requirements.txt file in your project. It's important to make sure anyone running your code is able to see what packages you are relying on",
    };
  };
}
