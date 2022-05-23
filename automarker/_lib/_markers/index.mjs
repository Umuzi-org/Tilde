import { markProject as pythonPytest } from "./pythonPytest/index.mjs";
import { markProject as pythonPytestOnlyOurTests } from "./pythonPytestOnlyOurTests/index.mjs";
import { markProject as javascriptJasmine } from "./javascriptJasmine/index.mjs";
import { markProject as javascriptJasmineOnlyOurTests } from "./javascriptJasmineOnlyOurTests/index.mjs";
import { markProject as javaJunit5 } from "./javaJunit5/index.mjs";
import { markProject as javaJunit5OnlyOurTests } from "./javaJunit5OnlyOurTests/index.mjs";

export const markers = {
  javascriptJasmine,
  javascriptJasmineOnlyOurTests,
  pythonPytest,
  pythonPytestOnlyOurTests,
  javaJunit5,
  javaJunit5OnlyOurTests,
};
