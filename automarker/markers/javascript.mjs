import { Marker, Step } from "./utils.mjs";

import Clone from "../actions/language-agnostic/clone-repo.mjs";
import CheckNodeModulesMissing from "../actions/javascript/check-node-modules-missing.mjs";
import CheckPackageJsonExists from "../actions/javascript/check-package-json-exists.mjs";
import CheckJasmineDevDependency from "../actions/javascript/check-jasmine-dev-dependency.mjs";
import DoNpmInstall from "../actions/javascript/do-npm-install.mjs";
import CopyJasmineTestRunner from "../actions/javascript/copy-jasmine-test-runner.mjs";
import CopyOurJasmineTests from "../actions/javascript/copy-our-tests.mjs";
import RunJasmineTests from "../actions/javascript/run-jasmine-tests.mjs";
import DoNpmInstallJasmine from "../actions/javascript/do-npm-install-jasmine.mjs";
import CheckNoImports from "../actions/javascript/check-no-imports.mjs";

export class JavascriptJasmine extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckNodeModulesMissing }),
    new Step({ Action: CheckPackageJsonExists }),
    new Step({ Action: CheckJasmineDevDependency }),
    new Step({ Action: DoNpmInstall }),
    new Step({ Action: CopyJasmineTestRunner }),
    new Step({ Action: RunJasmineTests, name: "running your tests" }),
    new Step({ Action: CopyOurJasmineTests }),
    new Step({ Action: RunJasmineTests, name: "running our tests" }),
  ];
}

export class JavascriptJasmineOnlyOurTests extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckNodeModulesMissing }),
    new Step({ Action: DoNpmInstallJasmine }),
    new Step({ Action: CopyJasmineTestRunner }),
    new Step({ Action: CopyOurJasmineTests }),
    new Step({ Action: RunJasmineTests, name: "running our tests" }),
  ];
}

export class JavascriptJasmineKatas extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: CheckNodeModulesMissing }),
    new Step({ Action: CheckNoImports }),
    new Step({ Action: DoNpmInstallJasmine }),
    new Step({ Action: CopyJasmineTestRunner }),
    new Step({ Action: CopyOurJasmineTests }),
    new Step({ Action: RunJasmineTests, name: "running our tests" }),
  ];
}
