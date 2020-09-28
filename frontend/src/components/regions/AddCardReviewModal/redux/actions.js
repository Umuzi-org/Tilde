import types from "./types.js";

export default {
  setProjectReviewOpenCardId: ({ cardId }) => {
    return { type: types.SET_PROJECT_REVIEW_OPEN_CARD_ID, cardId };
  },
};
