import { showButtons } from ".";

import {
  READY,
  IN_PROGRESS,
  // REVIEW_FEEDBACK,
  // IN_REVIEW,
  // COMPLETE,
} from "../../../../constants";

test("showButtons doesn't show addreview for topic", () => {
  const { showButtonAddReview } = showButtons({
    card: {
      reviewers: [],
      assignees: [1],
      contentType: "topic",
      status: IN_PROGRESS,
    },
    authUser: { isStaff: 1 },
    startAllowed: true,
  });

  expect(showButtonAddReview).toBe(false);
});

test("showButtons doesn't show request review for READY", () => {
  const { showButtonRequestReview } = showButtons({
    card: {
      reviewers: [],
      assignees: [1],
      contentType: "project",
      status: READY,
    },
    authUser: { isStaff: 1, userId: 1 },
    startAllowed: true,
  });

  expect(showButtonRequestReview).toBe(false);
});
