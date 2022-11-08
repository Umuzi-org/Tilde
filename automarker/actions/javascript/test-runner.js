#!/usr/bin/env node

const fs = require("fs");

const fileName = "test_output";
fs.writeFile(fileName, "", { flag: "w" }, (err) => {});

class FailedSpecNameReporter {
  constructor() {
    this.currentSpec = "No Spec";
  }

  jasmineStarted(suiteInfo) {}
  suiteStarted(result) {}
  specStarted(result) {
    this.currentSpec = result.fullName;

    fs.writeFileSync(
      fileName,
      `SPEC: ${this.currentSpec}\n`,
      { flag: "a+" },
      (err) => {}
    );
  }

  specDone(result) {
    if (result.failedExpectations.length > 0)
      fs.writeFileSync(
        fileName,
        `SPEC FAILED: ${this.currentSpec}\n${result.failedExpectations}`,
        { flag: "a+" },
        (err) => {}
      );
  }
  suiteDone(result) {}
  jasmineDone(result) {}
}

// setup Jasmine
const Jasmine = require("jasmine");
const jasmine = new Jasmine();
jasmine.loadConfig({
  spec_dir: "spec",
  spec_files: ["**/*[sS]pec.js"],
  helpers: ["helpers/**/*.js"],
  random: false,
  seed: null,
  stopSpecOnExpectationFailure: false,
});
jasmine.jasmine.DEFAULT_TIMEOUT_INTERVAL = 15000;

jasmine.env.clearReporters();

jasmine.addReporter(new FailedSpecNameReporter());

jasmine.execute();
