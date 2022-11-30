import React from "react";
import BaseReviewQueueEntry from "./BaseQueryEntry";

export default function PullRequestReviewQueueEntry({ project }) {
  console.log(
    project.recruitUserEmails,
    project.usersThatReviewedOpenPrsEmails
  );
  return (
    <BaseReviewQueueEntry
      project={project}
      showAllocatedReviewers={true}
      reviewers={project.usersThatReviewedOpenPrsEmails}
    />
  );
}
