import shell from "shelljs";
import { STATUS_FAIL } from "../consts.mjs";

export class Action {
  async execute({ test, ...params }) {
    let result = null;
    if (test && this.testAction) {
      result = this.testAction({ ...params });
    } else {
      result = this.action({ ...params });
    }
    result = await result;
    return result;
  }
}

/**
 * Call an async function with a maximum time limit (in milliseconds) for the timeout
 * @param {Promise<any>} asyncPromise An asynchronous promise to resolve
 * @param {number} timeLimit Time limit to attempt function in milliseconds
 * @returns {Promise<any> | undefined} Resolved promise for async function call, or an error if time limit reached
 */
export const asyncCallWithTimeout = async (
  asyncPromise,
  timeLimit = 180000
) => {
  let timeoutHandle;

  const timeoutPromise = new Promise((resolve, reject) => {
    timeoutHandle = setTimeout(
      () =>
        resolve({
          status: STATUS_FAIL,
          message:
            "This took very long to run. Are you sure it's not in an infinite loop?",
        }),
      timeLimit
    );
  });

  return Promise.race([asyncPromise, timeoutPromise]).then((result) => {
    clearTimeout(timeoutHandle);
    return result;
  });
};

export function execAsync(cmd, opts = {}) {
  return new Promise(function (resolve) {
    shell.exec(cmd, opts, function (code, stdout, stderr) {
      return resolve({ stdout, stderr, code });
    });
  });
}
