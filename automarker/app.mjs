// const { clone, review, listAllowedProjectChoices } = require("./lib");

import express from "express";
import cors from "cors";
import { STATUS_ERROR, STATUS_OK } from "./consts.mjs";
import { PORT } from "./env.mjs";
import { clone } from "./lib/index.mjs";

const app = express();
app.use(express.json());
app.use(cors());

app.get("/health-check", (req, res) => res.json({ status: STATUS_OK }));

app.post("/review-code", async function (req, res) {
  const { repoUrl, flavours, contentItemId } = req.body;

  if (!(repoUrl && flavours && contentItemId)) {
    // check that the arguments at least exist
    res.json({
      status: STATUS_ERROR,
      message:
        "Missing json arguments. API requires all of the following:\n\t- repoUrl\n\t- flavours\n\t- contentItemId",
    });
    return;
  }

  const cloneStatus = await clone({ repoUrl });

  if (cloneStatus.status === STATUS_ERROR) {
    res.json(cloneStatus);
    return;
  } else if (cloneStatus.status !== STATUS_OK) {
    throw Error(`Unknown status: ${cloneStatus}`);
  }
});

//   const contentItemIdClean = contentItemId.replace(/^\/|\/$/g, "");

//   res.json(
//     await review({
//       contentItemId: contentItemIdClean,
//       repoUrl,
//       flavours,
//     })
//   );
// });

app.listen(PORT, () => console.log(`Automarker listening on port ${PORT}!`));
