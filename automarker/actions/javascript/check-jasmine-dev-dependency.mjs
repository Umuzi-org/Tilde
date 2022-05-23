import { Action } from "../index.mjs";
import fs from "fs";
import { join } from "path";
import { STATUS_OK, STATUS_ERROR } from "../../consts.mjs";

export default class CheckJasmineDevDependency extends Action {
  name = "check jasmine dev dependency";
  action = async function ({ destinationPath }) {
    const path = join(destinationPath, "package.json");

    const packageJson = JSON.parse(fs.readFileSync(path, "utf8"));

    if (packageJson.devDependencies && packageJson.devDependencies.jasmine) {
      return { status: STATUS_OK };
    }

    if (packageJson.dependencies && packageJson.dependencies.jasmine) {
      return {
        status: STATUS_ERROR,
        message:
          "jasmine is listed as a regular dependency in your package. It should be a dev dependency. Take a look at this: https://nodejs.dev/learn/npm-dependencies-and-devdependencies",
      };
    }

    return {
      status: STATUS_ERROR,
      message:
        "jasmine is not listed as a dependency of your package. Please make sure you install it as a dev dependency",
    };
  };
}
