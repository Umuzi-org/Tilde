import { Marker, Step } from "./utils.mjs";

import Clone from "../actions/language-agnostic/clone-repo.mjs";
import NotImplemented from "../actions/language-agnostic/not-implemented.mjs";
import CheckNoImports from "../actions/java/check-no-imports.mjs";
import PrepForKataSelfTest from "../actions/java/prep-for-kata-self-test.mjs";
import PutKataFilesIntoPerfectProjectStructure from "../actions/java/put-kata-files-into-perfect-project-structure.mjs";
import RunJunitJupiterTests from "../actions/java/run-junit-jupiter-tests.mjs";

export class JavaJUnit5 extends Marker {
  steps = [new Step({ Action: Clone }), new Step({ Action: NotImplemented })];
}

export class JavaJUnit5OnlyOurTests extends Marker {
  steps = [new Step({ Action: Clone }), new Step({ Action: NotImplemented })];
}

export class JavaJUnit5Katas extends Marker {
  steps = [
    new Step({ Action: Clone }),
    new Step({ Action: PrepForKataSelfTest }),
    new Step({ Action: CheckNoImports }),
    new Step({ Action: PutKataFilesIntoPerfectProjectStructure }),
    new Step({ Action: RunJunitJupiterTests, name: "running our tests" }),
  ];
}
