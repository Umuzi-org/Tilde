import React from "react";
import BaseReviewQueueEntry from "./BaseQueryEntry";

export default function CompetenceReviewQueueEntry({ project }) {
  return (
    <BaseReviewQueueEntry
      project={project}
      showAllocatedReviewers={true}
      reviewers={project.usersThatReviewedSinceLastReviewRequestEmails}
    />
  );
}
