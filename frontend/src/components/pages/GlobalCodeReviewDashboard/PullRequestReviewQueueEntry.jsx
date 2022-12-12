import React from "react";
import BaseReviewQueueEntry from "./BaseQueryEntry";

export default function PullRequestReviewQueueEntry({ project }) {
  return (
    <BaseReviewQueueEntry
      project={project}
      showAllocatedReviewers={true}
      reviewers={project.usersThatReviewedOpenPrsEmails}
    />
  );
}
