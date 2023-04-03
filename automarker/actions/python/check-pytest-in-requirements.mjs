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
      console.log("===================");
      console.log(requirement);
      if (requirement.search(/^pytest/) !== -1)
        return {
          status: STATUS_OK,
        };
      console.log(requirement.includes("pytest"));
      if (requirement.includes("pytest") !== -1) {
        return {
          status: STATUS_FAIL,
          message: `Your requirements.txt file mentions pytest, but it is formatted incorrectly. There should be no characters before the word "pytest". If it looks right to you then please just delete the line and type it in by hand, sometimes special characters sneak in when you generate requirements files in strange ways.`,
        };
      }
    }
    return {
      status: STATUS_FAIL,
      message:
        "it looks like pytest is not in your requirements.txt file. Please make sure you install and use pytest appropriately. ",
    };
  };
}
