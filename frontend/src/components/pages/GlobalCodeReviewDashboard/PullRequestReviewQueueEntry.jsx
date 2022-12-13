import React from "react";
import BaseReviewQueueEntry from "./BaseQueryEntry";

export default function PullRequestReviewQueueEntry({ project }) {
  return (
    <BaseReviewQueueEntry
      project={project}
      showAllocatedReviewers={true}
      reviewerEmails={project.usersThatReviewedOpenPrsEmails}
      reviewerIds={project.usersThatReviewedOpenPrs}
    />
  );
}
