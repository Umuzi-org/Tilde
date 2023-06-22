// TODO: add an error message if config object is incorrect. Eg has missing perfect project path
// TODO: maybe change repoUrl to Url. We need to mark other kinds of projects
// TODO: rearchitect to make tests more DRY. Eg zmc site tests have a lot of repitition. Maybe allow copying tests from multiple locations

import express from "express";
import cors from "cors";
import { STATUS_ERROR, STATUS_OK, STATUS_MISSING_CONFIG } from "./consts.mjs";
import { PORT } from "./env.mjs";
import { getProjectConfig } from "./utils.mjs";
// import timeout from "connect-timeout"

import * as markers from "./markers/index.mjs";

const app = express();
app.use(express.json());
app.use(cors());

// function haltOnTimedout(){
//   if (!req.timedout) next();
// }

// app.use(timeout(`180s`)); // 3 minutes
// app.use(haltOnTimedout);

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
