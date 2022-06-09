import yaml from "js-yaml";
import fs from "fs";

import { CONFIGURATION_REPO_PATH } from "./env.mjs";

export function getProjectConfig({ contentItemId, flavours }) {
  console.log("getProjectConfig");
  console.log({ contentItemId, flavours });
  const configFilePath = `${CONFIGURATION_REPO_PATH}/config.yaml`;
  const allConfig = yaml.load(fs.readFileSync(configFilePath, "utf8"));

  const matchingConfig = allConfig
    .filter((o) => o.contentItemId === contentItemId)
    .filter((o) => arraysEqual(o.flavours, flavours));

  if (matchingConfig.length === 1) {
    const config = matchingConfig[0];
    console.log(config);
    return config;
  }
}

export function getMarker({ MarkerName }) {}

function arraysEqual(a, b) {
  a.sort();
  b.sort();
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length !== b.length) return false;

  for (var i = 0; i < a.length; ++i) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}
