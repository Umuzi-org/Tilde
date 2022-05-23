import { Action } from "../index.mjs";
import fs from "fs";
import { join } from "path";
import { STATUS_OK, STATUS_ERROR } from "../../consts.mjs";

export default class CheckNodeModulesMissing extends Action {
  name = "check node_modules missing";
  action = async function ({ destinationPath }) {
    const path = join(destinationPath, "node_modules");

    if (fs.existsSync(path)) {
      return {
        status: STATUS_ERROR,
        message:
          "node_modules found inside your repo. Did you forget to use gitignore? Please make sure that node_modules are never ever included in your project submissions",
      };
    }

    return {
      status: STATUS_OK,
    };
  };
}
