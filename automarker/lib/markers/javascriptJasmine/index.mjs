import { markProjectBase } from "../utils.mjs";

export function markProject({ fullPerfectProjectPath, fullClonePath }) {
  return markProjectBase({
    fullPerfectProjectPath,
    fullClonePath,
    lookForTestProblems,
    markerName: "javascriptJasmine",
  });
}

function lookForTestProblems(testOutput) {
  let errors = [];

  console.log("xxxxxxxxxxxxxxxxxx");
  console.log("xxxxxxxxxxxxxxxxxx");
  console.log(testOutput);
  console.log("xxxxxxxxxxxxxxxxxx");
  console.log("xxxxxxxxxxxxxxxxxx");

  if (testOutput.indexOf("jasmine: command not found") != -1) {
    console.error("jasmine: command not found");
    return ["jasmine: command not found"];
  }

  const counts = testOutput.match(/(\d+) specs{0,1}, (\d+) failures{0,1}/);
  if (counts) {
    const specs = parseInt(counts[1]);
    const failures = parseInt(counts[2]);

    if (specs === 0) {
      errors.push("There are zero specs");
    }
    if (failures > 0) {
      //   errors.push(`There are ${failures} failing tests!`);
      errors.push(testOutput);
      // TODO: don't be so verbose, rather just return short stings eg:
      // failed test "simple calculator should add as many numbers as I want"
    }

    return errors;
  }

  const moduleNotFound = testOutput.match(/(Error: Cannot find module .*)\n/);
  if (moduleNotFound) {
    return [moduleNotFound[1]];
  }

  if (testOutput.indexOf("No specs found") !== -1) {
    return ["No specs found. Are you sure you called jasmine init?"];
  }

  return errors;
}
