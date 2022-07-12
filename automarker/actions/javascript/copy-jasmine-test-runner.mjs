import { Action } from "../index.mjs";
import fs from "fs";
import { join } from "path";

import { STATUS_OK } from "../../consts.mjs";

export default class CopyJasmineTestRunner extends Action {
  name = "copy jasmine test runner";
  action = async function ({ destinationPath }) {
    const source = "./actions/javascript/test-runner.js";
    const destination = join(destinationPath, "test-runner.js");

    fs.copyFileSync(source, destination);
    return { status: STATUS_OK };
  };
}
