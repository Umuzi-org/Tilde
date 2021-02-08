import React from "react";

import ErrorOutlineIcon from "@material-ui/icons/ErrorOutline";
import HighlightOffIcon from "@material-ui/icons/HighlightOff";
import CheckCircleOutlineIcon from "@material-ui/icons/CheckCircleOutline";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import { Tooltip } from "@material-ui/core";

import { INCORRECT, CORRECT, CONTRADICTED } from "../../constants";

const TrustedIcon = CheckCircleIcon;
const ReviewValidatedIcons = {
  [INCORRECT]: HighlightOffIcon,
  [CORRECT]: CheckCircleOutlineIcon,
  [CONTRADICTED]: ErrorOutlineIcon,
};

const reviewValidatedHelptext = {
  [INCORRECT]: "a trusted user disagrees with this. It is definately wrong",
  [CORRECT]: "a trusted reviewer agrees with this",
  [CONTRADICTED]: "someone contradicted this review. It might be wrong",
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
