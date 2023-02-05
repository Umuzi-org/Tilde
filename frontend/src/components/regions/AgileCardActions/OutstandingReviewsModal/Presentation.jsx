import { Card, CardContent, Typography } from "@material-ui/core";
import React from "react";
import FlavourChips from "../../../widgets/FlavourChips";
import TagChips from "../../../widgets/TagChips";
import { getAgeString } from "../../../widgets/utils";
import MoreIcon from "@material-ui/icons/More";
import { routes } from "../../../../routes";
import CardButton from "../../../widgets/CardButton";
import Modal from "../../../widgets/Modal";

export default function Presentation({
  cardsNeedingCompetenceReview,
  open,
  handleClose,
}) {
  return (
    <Modal
      open={open}
      onClose={handleClose}
      title="There are people waiting for your feedback"
    >
      <Typography>
        Your colleagues need your feedback so that they can move forward with
        their work. When reviewing other people's work it's important that you
        pay close attention and do a good job. We review each other's work in
        order to maximize learning.
      </Typography>
      <Typography>Please review the following cards:</Typography>

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
