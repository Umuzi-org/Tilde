import { Marker, Step } from "./utils.mjs";

import Clone from "../actions/language-agnostic/clone-repo.mjs";

export class JavaJUnit5 extends Marker {
  steps = [new Step({ Action: Clone })];
}

export class JavaJUnit5OnlyOurTests extends Marker {
  steps = [new Step({ Action: Clone })];
}

export class JavaJUnit5Katas extends Marker {
  steps = [new Step({ Action: Clone })];
}
