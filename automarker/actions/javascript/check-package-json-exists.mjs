import { Action } from "../index.mjs";
import fs from "fs";
import { join } from "path";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class CheckPackageJsonExists extends Action {
  name = "check package.json exists";
  action = async function ({ destinationPath }) {
    const path = join(destinationPath, "package.json");

    if (fs.existsSync(path)) {
      return {
        status: STATUS_OK,
      };
    }

    return {
      status: STATUS_FAIL,
      message:
        "Looks like you didn't include a package.json file in your project. Take a look at this: https://docs.npmjs.com/cli/v8/commands/npm-init",
    };
  };
}
