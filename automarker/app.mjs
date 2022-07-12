// const { clone, review, listAllowedProjectChoices } = require("./lib");

import express from "express";
import cors from "cors";
import { STATUS_ERROR, STATUS_OK, STATUS_MISSING_CONFIG } from "./consts.mjs";
import { PORT } from "./env.mjs";
import { getProjectConfig } from "./utils.mjs";

import * as markers from "./markers/index.mjs";

const app = express();
app.use(express.json());
app.use(cors());

app.get("/health-check", (req, res) => res.json({ status: STATUS_OK }));

app.post("/test-config", async function (req, res) {
  const { flavours, contentItemId } = req.body;

  // check that the arguments at least exist
  if (!(flavours && contentItemId)) {
    res.json({
      status: STATUS_ERROR,
      message:
        "Missing json arguments. API requires all of the following:\n\t- repoUrl\n\t- flavours\n\t- contentItemId",
    });
    return;
  }

  const config = getProjectConfig({ flavours, contentItemId });

  if (config === undefined) {
    res.json({
      status: STATUS_MISSING_CONFIG,
      message: "There is no matching configuration",
    });
    return;
  }

  // {
  //   contentItemId: 273,
  //   flavours: [ 'javascript' ],
  //   perfectProjectPath: 'projects/simple_calculator_js',
  //   marker: 'javascriptJasmine'
  // }

  const Marker = markers[config.marker];

  if (!Marker) {
    res.json({
      status: STATUS_MISSING_CONFIG,
      message: `No marker named ${config.marker}`,
    });
    return;
  }

  const marker = new Marker();

  res.json(
    await marker.mark({
      test: true,
      perfectProjectPath: config.perfectProjectPath,
    })
  );
});

app.post("/mark-project", async function (req, res) {
  const { flavours, contentItemId, repoUrl } = req.body;

  // check that the arguments at least exist
  if (!(flavours && contentItemId)) {
    res.json({
      status: STATUS_ERROR,
      message:
        "Missing json arguments. API requires all of the following:\n\t- repoUrl\n\t- flavours\n\t- contentItemId",
    });
    return;
  }

  const config = getProjectConfig({ flavours, contentItemId });

  if (config === undefined) {
    res.json({
      status: STATUS_MISSING_CONFIG,
      message: "There is no matching configuration",
    });
    return;
  }

  const Marker = markers[config.marker];

  if (!Marker) {
    res.json({
      status: STATUS_MISSING_CONFIG,
      message: `No marker named ${config.marker}`,
    });
    return;
  }

  const marker = new Marker();

  res.json(
    await marker.mark({
      test: false,
      perfectProjectPath: config.perfectProjectPath,
      repoUrl,
    })
  );
});

// app.post("/mark-project", async function (req, res) {
//   const { repoUrl, flavours, contentItemId } = req.body;

//   // check that the arguments at least exist
//   if (!(repoUrl && flavours && contentItemId)) {
//     res.json({
//       status: STATUS_ERROR,
//       message:
//         "Missing json arguments. API requires all of the following:\n\t- repoUrl\n\t- flavours\n\t- contentItemId",
//     });
//     return;
//   }

//   const config = getProjectConfig({ flavours, contentItemId });

//   if (config === undefined) {
//     res.json({
//       status: STATUS_MISSING_CONFIG,
//       message: "There is no matching configuration",
//     });
//     return;
//   }

//   const marker = getMarker();

//   res.json(
//     await marker.mark({
//       repoUrl,
//     })
//   );
// });

app.listen(PORT, () => console.log(`Auto-marker listening on port ${PORT}!`));
