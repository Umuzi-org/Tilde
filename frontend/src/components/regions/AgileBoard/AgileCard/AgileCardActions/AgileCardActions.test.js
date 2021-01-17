import { showButtons } from "./utils";

import {
  READY,
  IN_PROGRESS,
  BLOCKED,
  REVIEW_FEEDBACK,
  IN_REVIEW,
  COMPLETE,
} from "../../../../../constants";

test("showButtons shows DOESNT show start project on topics", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: true,
    canForceStart: true,
    assignees: [authUser.userId],
    contentTypeNice: "topic",
  };
  const { showButtonStartProject } = showButtons({ authUser, card });
  expect(showButtonStartProject).toBe(false);
});

test("showButtons shows start project button to assignee if start is allowed", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: true,
    canForceStart: true,
    assignees: [authUser.userId],
    contentTypeNice: "project",
  };
  const { showButtonStartProject } = showButtons({ authUser, card });
  expect(showButtonStartProject).toBe(true);
});

test("showButtons DOES NOT show start project button to non assignees with no special flags", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: true,
    canForceStart: true,
    assignees: [authUser.userId + 1],
    contentTypeNice: "project",
  };
  const { showButtonStartProject } = showButtons({ authUser, card });
  expect(showButtonStartProject).toBe(false);
});

test("showButtons DOES show start project button to superusers", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: true,
    assignees: [authUser.userId + 1],
    contentTypeNice: "project",
  };
  const { showButtonStartProject } = showButtons({ authUser, card });
  expect(showButtonStartProject).toBe(true);
});

test("showButtons DOES NOT show start project button to superusers if  forceStart is false", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: false,
    assignees: [authUser.userId + 1],
    contentTypeNice: "project",
  };
  const { showButtonStartProject } = showButtons({ authUser, card });
  expect(showButtonStartProject).toBe(false);
});

test("showButtons DOES NOT show start project button to assignee if start is NOT allowed", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: true,
    assignees: [authUser.userId],
    contentTypeNice: "project",
  };
  const { showButtonStartProject } = showButtons({ authUser, card });
  expect(showButtonStartProject).toBe(false);
});

test("showButton returns showButtonNoteWorkshopAttendance=False for people without manage permission", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: false,
    assignees: [authUser.userId],
    contentTypeNice: "workshop",
    status: READY,
  };

  const {
    showButtonNoteWorkshopAttendance,
    showButtonCancelWorkshopAttendance,
  } = showButtons({ authUser, card });
  expect(showButtonNoteWorkshopAttendance).toBe(false);
  expect(showButtonCancelWorkshopAttendance).toBe(false);
});

test("showButton shows showButtonNoteWorkshopAttendance for people with manage permission if WORKSHOP card is READY", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: false,
    assignees: [authUser.userId + 1],
    contentTypeNice: "workshop",
    status: READY,
  };

  const {
    showButtonNoteWorkshopAttendance,
    showButtonCancelWorkshopAttendance,
  } = showButtons({ authUser, card });
  expect(showButtonNoteWorkshopAttendance).toBe(true);
  expect(showButtonCancelWorkshopAttendance).toBe(false);
});

test("showButton shows showButton NoteWorkshopAttendance for people with manage permission if WORKSHOP card is BLOCKED", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: false,
    assignees: [authUser.userId + 1],
    contentTypeNice: "workshop",
    status: BLOCKED,
  };

  const {
    showButtonNoteWorkshopAttendance,
    showButtonCancelWorkshopAttendance,
  } = showButtons({ authUser, card });
  expect(showButtonNoteWorkshopAttendance).toBe(true);
  expect(showButtonCancelWorkshopAttendance).toBe(false);
});

test("showButton returns showButtonStartTopic=true for card assignee if canStart", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: true,
    canForceStart: true,
    assignees: [authUser.userId],
    contentTypeNice: "topic",
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(true);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonStartTopic=false for card assignee if status is NOT canStart", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: true,
    assignees: [authUser.userId],
    contentTypeNice: "topic",
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonStartTopic=true for card manager with forceStart ", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: true,
    assignees: [authUser.userId + 1],
    contentTypeNice: "topic",
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(true);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonStartTopic=false for card manager without forceStart ", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    canStart: false,
    canForceStart: false,
    assignees: [authUser.userId + 1],
    contentTypeNice: "topic",
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonStartTopic=false for arb user without forceStart ", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    canStart: true,
    canForceStart: true,
    assignees: [authUser.userId + 1],
    contentTypeNice: "topic",
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonEndTopic=true showButtoStopTopic=true for card assignee if status is IN_PROGRESS", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    status: IN_PROGRESS,
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
    showButtonRequestReview,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(true);
  expect(showButtonEndTopic).toBe(true);
  expect(showButtonRequestReview).toBe(false);
});

test("showButton returns showButtonEndTopic=false showButtonStopopic=false for card assignee if status is NOT IN_PROGRESS", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    //   status: IN_PROGRESS,
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonEndTopic=true showButtoStopTopic=true for card manager if status is IN_PROGRESS", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId + 1],
    contentTypeNice: "topic",
    status: IN_PROGRESS,
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
    showButtonRequestReview,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(true);
  expect(showButtonRequestReview).toBe(false);
  expect(showButtonEndTopic).toBe(true);
});

test("showButton returns showButtonEndTopic=false showButtonRequestReview=true for card assignee if status is IN_PROGRESS and TOPIC NEEDS REVIEW", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    status: IN_PROGRESS,
    topicNeedsReview: true,
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
    showButtonRequestReview,
  } = showButtons({ authUser, card });

  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(true);
  expect(showButtonRequestReview).toBe(true);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonEndTopic=false showButtonStopopic=false for card manager if status is NOT IN_PROGRESS", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],

    assignees: [authUser.userId + 1],
    contentTypeNice: "topic",
    //   status: IN_PROGRESS,
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});
test("showButton returns showButtonEndTopic=false showButtonStopopic=false for card arbitrary user if status is IN_PROGRESS", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId + 1],
    contentTypeNice: "topic",
    status: IN_PROGRESS,
  };

  const {
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,
  } = showButtons({ authUser, card });
  expect(showButtonStartTopic).toBe(false);
  expect(showButtonStopTopic).toBe(false);
  expect(showButtonEndTopic).toBe(false);
});

test("showButton returns showButtonAddReview=true if user is reviewer and PROJECT card status is IN_REVIEW", () => {
  const authUser = { userId: 3 };
  const card = {
    assignees: [],
    reviewers: [authUser.userId],
    contentTypeNice: "project",
    status: IN_REVIEW,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(true);
});

test("showButton returns showButtonAddReview=true if user is reviewer and PROJECT card status is COMPLETE", () => {
  const authUser = { userId: 3 };
  const card = {
    assignees: [],
    reviewers: [authUser.userId],
    contentTypeNice: "project",
    status: COMPLETE,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(true);
});

test("showButton returns showButtonAddReview=true if user is reviewer and PROJECT card status is REVIEW_FEEDBACK", () => {
  const authUser = { userId: 3 };
  const card = {
    assignees: [],
    reviewers: [authUser.userId],
    contentTypeNice: "project",
    status: REVIEW_FEEDBACK,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(true);
});

test("showButton returns showButtonAddReview=true if user has reviewer permission and PROJECT card status is IN_REVIEW", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    assignees: [],
    reviewers: [],
    contentTypeNice: "project",
    status: IN_REVIEW,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(true);
});

test("showButton returns showButtonAddReview=false if user is not reviewer and PROJECT card status is IN_REVIEW", () => {
  const authUser = { userId: 3 };
  const card = {
    assignees: [],
    reviewers: [],
    contentTypeNice: "project",
    status: IN_REVIEW,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(false);
});

test("showButton returns showButtonAddReview=true if user is reviewer and TOPIC card status is IN_REVIEW", () => {
  const authUser = { userId: 3 };
  const card = {
    assignees: [],
    reviewers: [authUser.userId],
    contentTypeNice: "topic",
    topicNeedsReview: true,
    status: IN_REVIEW,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(true);
});

test("showButton returns showButtonAddReview=false if user is reviewer and TOPIC card status is IN_REVIEW but NOT topicNeedsReview", () => {
  const authUser = { userId: 3 };
  const card = {
    assignees: [],
    reviewers: [authUser.userId],
    contentTypeNice: "topic",
    //   topicNeedsReview: ,
    status: IN_REVIEW,
  };
  const { showButtonAddReview } = showButtons({ authUser, card });
  expect(showButtonAddReview).toBe(false);
});

test("showButton returns showButtonRequestReview=true showButtonCancelReviewRequest=false for Project cards IN_PROGRESS for assignee", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "project",
    status: IN_PROGRESS,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(true);
  expect(showButtonCancelReviewRequest).toBe(false);
});
test("showButton returns showButtonRequestReview=true showButtonCancelReviewRequest=false for Topic cards IN_PROGRESS for assignee, if needs review", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    topicNeedsReview: true,
    status: IN_PROGRESS,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(true);
  expect(showButtonCancelReviewRequest).toBe(false);
});

test("showButton returns showButtonRequestReview=false showButtonCancelReviewRequest=false for Topic cards IN_PROGRESS for assignee, if NOT needs review", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    //   topicNeedsReview: true,
    status: IN_PROGRESS,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(false);
  expect(showButtonCancelReviewRequest).toBe(false);
});

test("showButton returns showButtonRequestReview=false showButtonCancelReviewRequest=true for Project cards IN_REVIEW for assignee", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "project",
    status: IN_REVIEW,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(false);
  expect(showButtonCancelReviewRequest).toBe(true);
});
test("showButton returns showButtonRequestReview=false showButtonCancelReviewRequest=true for Topic cards IN_REVIEW for assignee, if needs review", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    topicNeedsReview: true,
    status: IN_REVIEW,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(false);
  expect(showButtonCancelReviewRequest).toBe(true);
});

test("showButton returns showButtonRequestReview=false showButtonCancelReviewRequest=false for Topic cards IN_REVIEW for assignee, if NOT needs review", () => {
  const authUser = { userId: 3 };
  const card = {
    reviewers: [],
    assignees: [authUser.userId],
    contentTypeNice: "topic",
    //   topicNeedsReview: true,
    status: IN_REVIEW,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(false);
  expect(showButtonCancelReviewRequest).toBe(false);
});

test("showButton returns showButtonRequestReview=false showButtonCancelReviewRequest=true for Project cards IN_REVIEW for manager", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    assignees: [],
    contentTypeNice: "project",
    status: IN_REVIEW,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(false);
  expect(showButtonCancelReviewRequest).toBe(true);
});

test("showButton returns showButtonRequestReview=true showButtonCancelReviewRequest=false for Topic cards IN_PROGRESS for manager, if needs review", () => {
  const authUser = { userId: 3, isSuperuser: 1 };
  const card = {
    reviewers: [],
    assignees: [],
    contentTypeNice: "topic",
    topicNeedsReview: true,
    status: IN_PROGRESS,
  };
  const {
    showButtonRequestReview,
    showButtonCancelReviewRequest,
  } = showButtons({ authUser, card });
  expect(showButtonRequestReview).toBe(true);
  expect(showButtonCancelReviewRequest).toBe(false);
});
