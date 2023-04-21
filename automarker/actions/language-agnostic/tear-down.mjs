import shell from "shelljs";
import { CLONE_PATH } from "../../env.mjs";
import { STATUS_OK, STATUS_ERROR } from "../../consts.mjs";
import { Action } from "../index.mjs";
import fs from "fs";

export default class Cleanup extends Action {
  name = "cleanup";

  action = async function ({ destinationPath }) {
    console.log(`deleting... ${destinationPath}`);

    if (fs.existsSync(destinationPath)) {
      console.log("exists!");
      fs.rmSync(destinationPath, { recursive: true, force: true });
    }

    return {
      status: STATUS_OK,
    };
  };
}
