import React from "react";
import BaseReviewQueueEntry from "./BaseQueryEntry";

export default function PullRequestReviewQueueEntry({ project, card }) {
  console.log(project.openPrCount);
  return (
    <BaseReviewQueueEntry
      project={project}
      //showAllocatedReviewers={true}
    />
  );
}
