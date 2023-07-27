import { Action, asyncCallWithTimeout, execAsync } from "../index.mjs";
import { STATUS_OK, STATUS_FAIL } from "../../consts.mjs";

export default class RunJunitJupiterTests extends Action {
  name = "junit jupiter tests";

  action = async function ({ destinationPath }) {
    const scriptPath = "./actions/java/run-junit-jupiter-tests.sh";

    const command = `DESTINATION_PATH=${destinationPath} bash -c ${scriptPath}`;

    const scriptOutputPromise = execAsync(command);

    const scriptOutput = await asyncCallWithTimeout(scriptOutputPromise);

    if (scriptOutput.status === STATUS_FAIL) return scriptOutput;

    const problems = lookForTestProblems(
      scriptOutput.stdout,
      scriptOutput.stderr
    );

    if (problems.length) {
      return {
        status: STATUS_FAIL,
        message: "Unit test errors",
        errors: problems,
      };
    } else {
      return {
        status: STATUS_OK,
      };
    }
  };
}

function lookForTestProblems(standardOut, standardErr) {
  if (standardOut.match("BUILD SUCCESSFUL")) return [];

  console.log("=========================================");
  console.log("=========================================");
  console.log(standardErr);
  console.log("=========================================");
  console.log("=========================================");

  if (standardErr.match("error: cannot find symbol")) {
    return [
      "We are trying to test your code but can't. Something isn't named correctly. Please check that your file name, class name, function name and package are all 100% correct. They should match the project specification exactly",
    ];
  }

  if (
    standardErr.match(
      "error: class .* is public, should be declared in a file named .*.java"
    )
  ) {
    return [
      "It looks like your file name and class name don't match. If you have a public class named Foo then it should be defined in a file named Foo.java",
    ];
  }

  if (
    standardErr.match(
      "error: non-static method .* cannot be referenced from a static context"
    )
  ) {
    return [
      "One of the functions under test is meant to be static, but it isn't. For example if you your function is named foo you should do this: `public static void foo(`",
    ];
  }

  const testErrors = [...standardOut.matchAll(/<>(.*)<\/>/g)].map(
    (match) => match[1]
  );

  if (testErrors.length) return testErrors;

  const remainingErrors = [
    ...standardErr.matchAll(/.*\/.*java:\d*: error: (.*)\n/g),
  ]
    .map((match) => match[1])
    .map((err) => {
      if (err.match("incompatible types"))
        return `${err}. It looks like one of your functions doesn't accept the right types of arguments, or it might be returning the wrong thing`;
      if (err.match("cannot be applied to given types"))
        return `${err}. It looks like one of your functions doesn't accept the right types of arguments, or it might be returning the wrong thing`;
      if (err.match("no suitable method found"))
        return `${err}. It looks like you need to overload your function. Make sure it can be called exactly as described in the project specification.`;
      if (err.match("type not allowed here"))
        return `${err}. It looks like you are using the wrong datatype somewhere. Double check all your function arguments and returned values`;

      throw new Error(`Unhandled error:\n\n${err}`);
    });

  if (remainingErrors.length) return remainingErrors;

  if (standardErr.match("FAILURE: Build failed with an exception."))
    return [
      "Something went wrong when we tried to test your code. Please make sure you are using all the right data-types for your function arguments and returns. You need to write code that exactly matches the specification!",
    ];

  throw new Error(`Unhandled failure:\n\n'''\n${standardErr}\n'''`);
}
