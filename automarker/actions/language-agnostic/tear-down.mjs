import { STATUS_OK } from "../../consts.mjs";
import { Action } from "../index.mjs";
import fs from "fs";
import { SKIP_TEARDOWN } from "../../env.mjs";

export default class Teardown extends Action {
  name = "cleaning up";

  action = async function ({ destinationPath }) {
    if (SKIP_TEARDOWN) {
      console.log("skipping teardown");
      return {
        status: STATUS_OK,
      };
    }

    console.log(`deleting... ${destinationPath}`);
    console.log({ destinationPath });

    if (fs.existsSync(destinationPath)) {
      console.log("exists!");
      fs.rmSync(destinationPath, { recursive: true, force: true });
    }

    return {
      status: STATUS_OK,
    };
  };
}
