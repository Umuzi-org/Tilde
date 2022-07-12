import { Action } from "../index.mjs";
import { STATUS_FAIL, STATUS_OK } from "../../consts.mjs";
import fs from "fs";
import { join } from "path";

export default class CheckPytestInRequirements extends Action {
  name = "checking that pytest is in your requirements.txt file";
  action = async function ({ destinationPath }) {
    const path = join(destinationPath, "requirements.txt");

    const requirements = fs
      .readFileSync(path, "utf8")
      .split("\n")
      .map((row) => row.trim());

    for (let requirement of requirements) {
      if (requirement.match(/^pytest/))
        return {
          status: STATUS_OK,
        };
    }
    return {
      status: STATUS_FAIL,
    };
  };
}
