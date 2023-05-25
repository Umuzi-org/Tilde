import Creators from "./actions.js";

export default {
  ...Creators,

  openCardReviewForm: ({ cardId }) => {
    return Creators.setProjectReviewOpenCardId({ cardId: parseInt(cardId) });
  },
  closeCardReviewForm: () =>
    Creators.setProjectReviewOpenCardId({ cardId: null }),
};
