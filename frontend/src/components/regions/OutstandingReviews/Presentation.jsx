import { Card, CardContent, Typography } from "@material-ui/core";
import React from "react";
import FlavourChips from "../../../widgets/FlavourChips";
import TagChips from "../../../widgets/TagChips";
import { getAgeString } from "../../../widgets/utils";
import MoreIcon from "@material-ui/icons/More";
import { routes } from "../../../../routes";
import CardButton from "../../../widgets/CardButton";

import Modal from "../../../widgets/Modal";

export default function Presentation({ cardsNeedingCompetenceReview }) {
  return (
    <Modal open={true} onClose={() => 1}>
      <Typography variant="h3" gutterBottom>
        People are awaiting your feedback
      </Typography>
      <Typography>
        The following cards need your review. You need to complete your reviews
        before you can move on with your own assigned cards.
      </Typography>

      {cardsNeedingCompetenceReview.map((card) => (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6">{card.title}</Typography>
            <TagChips tagNames={card.tagNames} />
            <FlavourChips flavourNames={card.flavourNames} />
            <Typography variant="subtitle2">Assignee:</Typography>
            <Typography>{card.assigneeNames}</Typography>

            <Typography>
              Review requested: {getAgeString(card.reviewRequestTime)}
            </Typography>

            <a href={routes.cardDetails.route.path.replace(":cardId", card.id)}>
              <CardButton label="Details" startIcon={<MoreIcon />} />{" "}
            </a>
          </CardContent>
        </Card>
      ))}
    </Modal>
  );
}
