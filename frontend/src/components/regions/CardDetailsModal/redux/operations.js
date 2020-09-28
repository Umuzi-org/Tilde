import Creators from "./actions.js";

export default {
  ...Creators,
  openCardDetailsModal: ({ cardId }) =>
    Creators.setCardDetaisModalOpen({ cardId }),
  closeCardDetailsModal: () =>
    Creators.setCardDetaisModalOpen({ cardId: null }),
};
