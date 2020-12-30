import React from "react";

import CardDetailsModal from "../components/regions/CardDetailsModal/Presentation";
import reviewObject from "./assets/review.json";

export default {
  title: "Tilde/CardDetailsModal/CardDetailsModal",
  component: CardDetailsModal,
  argTypes: {
    //   backgroundColor: { control: 'color' },
  },
};

const Template = (args) => <CardDetailsModal {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  cardId: 1,
  card: {
    id: 13095,
    contentItem: 223,
    contentItemUrl:
      "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/projects/oop/person/_index.md",
    status: "RF",
    recruitProject: 2652,
    assignees: [285],
    reviewers: [72, 67, 294, 297],
    assigneeNames: ["kabelomg@gmail.com"],
    reviewerNames: [
      "lethabo.letsoalo@umuzi.org",
      "lentswe.mamonong@umuzi.org",
      "baloyimahlori@gmail.com",
      "manelisi.madini@umuzi.org",
    ],
    isHardMilestone: false,
    isSoftMilestone: false,
    title: "Person",
    contentType: "project",
    storyPoints: 2,
    tagNames: ["oop"],
    order: 18,
    codeReviewCompetentSinceLastReviewRequest: 1,
    codeReviewExcellentSinceLastReviewRequest: 0,
    codeReviewRedFlagSinceLastReviewRequest: 0,
    codeReviewNyCompetentSinceLastReviewRequest: 3,
    requiresCards: [],
    requiredByCards: [13096],
    flavourNames: ["javascript"],
    projectSubmissionTypeNice: "repo",
    topicNeedsReview: false,
    topicProgress: null,
    dueTime: null,
    completeTime: null,
    reviewRequestTime: "2020-09-30T11:56:56.813622Z",
    startTime: null,
  },
  reviews: [reviewObject],
  reviewIds: [1],
};
