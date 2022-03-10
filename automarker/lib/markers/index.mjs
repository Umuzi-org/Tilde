import { markProject as pythonPytest } from "./pythonPytest/index.mjs";
import { markProject as javascriptJasmine } from "./javascriptJasmine/index.mjs";
import { markProject as javaJunit5 } from "./javaJunit5/index.mjs";

export const markers = {
  javascriptJasmine,
  pythonPytest,
  javaJunit5,
};
