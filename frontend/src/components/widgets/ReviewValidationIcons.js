import React from "react";

import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { Tooltip } from "@material-ui/core";

import { INCORRECT, CORRECT, CONTRADICTED } from "../../constants";

const TrustedIcon = CheckCircleIcon;
const ReviewValidatedIcons = {
  [INCORRECT]: HighlightOffIcon,
  [CORRECT]: CheckCircleOutlineIcon,
  [CONTRADICTED]: HelpOutlineIcon,
};

const reviewValidatedHelptext = {
  [INCORRECT]: "a trusted user disagrees with this. It is definately wrong",
  [CORRECT]: "a trusted reviewer agrees with this. Well done :)",
  [CONTRADICTED]: "someone disagrees with you. There's a lesson here for you",
  trusted: "the reviewing user is trusted for this project",
};

export default ({ review }) => {
  const ValidatedIcon = review.validated
    ? ReviewValidatedIcons[review.validated]
    : null;

  const helptext = review.validated
    ? reviewValidatedHelptext[review.validated]
    : null;

  return (
    <React.Fragment>
      {review.trusted && (
        <Tooltip title={reviewValidatedHelptext.trusted}>
          <TrustedIcon />
        </Tooltip>
      )}
      {helptext && (
        <Tooltip title={helptext}>
          <ValidatedIcon />
        </Tooltip>
      )}
    </React.Fragment>
  );
};
