import shell from "shelljs";
import { STATUS_OK, STATUS_ERROR } from "../../consts.mjs";
import { Action } from "../index.mjs";

/*Take the perfect project and get it into the same structure that the learner would have needed to use. So that basically means remove all the fancy gradle stuff and just leave the .java source files. This is only useful for self-checking configuration */
export default class PrepForKataSelfTest extends Action {
  name = "prep for kata self test";

  action = async function () {
    return {
      status: STATUS_OK,
    };
  };

  testAction = async function ({ destinationPath }) {
    const scriptPath = "./actions/java/prep-for-kata-self-test.sh";
    const command = `DESTINATION_PATH=${destinationPath} bash -c ${scriptPath}`;
    await shell.exec(command).stdout;

    return {
      status: STATUS_OK,
    };
  };
}
