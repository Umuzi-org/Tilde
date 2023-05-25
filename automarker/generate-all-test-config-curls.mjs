import yaml from "js-yaml";
import fs from "fs";

import { CONFIGURATION_REPO_PATH } from "./env.mjs";

const configFilePath = `${CONFIGURATION_REPO_PATH}/config.yaml`;
const allConfig = yaml.load(fs.readFileSync(configFilePath, "utf8"));

allConfig
  .filter((o) => o.mode == "debug" || o.mode == "prod")
  .forEach((o) => {
    console.log(`curl \
--request POST \
--header "Content-Type: application/json" \
--data '{"contentItemId":${o.contentItemId}, "flavours": ${JSON.stringify(
      o.flavours
    )}}' \
http://localhost:1337/test-config
    `);
  });
