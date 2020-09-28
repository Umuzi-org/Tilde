import React from "react";

import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
// import CardHeader from "@material-ui/core/CardHeader";
import { Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import MoreIcon from "@material-ui/icons/More";

import CardButton from "../../../../widgets/CardButton";
import CardReviewBadges from "../../../../widgets/CardReviewBadges";

import {
  AGILE_CARD_STATUS_CHOICES,
  BLOCKED,
  READY,
  IN_PROGRESS,
  REVIEW_FEEDBACK,
  IN_REVIEW,
  COMPLETE,
} from "../../../../../constants";

import yellow from "@material-ui/core/colors/yellow";
import orange from "@material-ui/core/colors/orange";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import grey from "@material-ui/core/colors/grey";
import blue from "@material-ui/core/colors/blue";

const useStyles = makeStyles((theme) => {
  const card = {
    width: "100%",
    borderWidth: theme.spacing(0.5),
  };

  return {
    [BLOCKED]: { ...card, borderColor: grey[400] },
    [READY]: { ...card, borderColor: blue[400] },
    [IN_PROGRESS]: { ...card, borderColor: green[400] },
    [REVIEW_FEEDBACK]: { ...card, borderColor: red[400] },
    [IN_REVIEW]: { ...card, borderColor: orange[400] },
    [COMPLETE]: { ...card, borderColor: yellow[400] },

    cardHeader: {
      padding: theme.spacing(1),
    },

    status: {
      padding: theme.spacing(1),
    },

    cardId: {},
  };
});

export default ({ handleClickOpenDetails, card }) => {
  if (card === undefined) {
    return <React.Fragment />;
  }
  const classes = useStyles();

  return (
    <Card className={classes[card.status]} variant="outlined">
      <CardContent>
        <CardReviewBadges card={card} />
        <Typography className="cardId" variant="caption">
          [id:{card.id}]
        </Typography>
        <Typography className="status">
          {AGILE_CARD_STATUS_CHOICES[card.status]}
        </Typography>

        {card.recruitProject && (
          <CardButton
            label="Details"
            startIcon={<MoreIcon />}
            onClick={handleClickOpenDetails}
          />
        )}
      </CardContent>
    </Card>
  );
};
