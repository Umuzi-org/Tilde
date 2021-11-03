import types from "./types.js";

export default {
  setCardDetaisModalOpen: ({ cardId }) => {
    return { type: types.SET_CARD_DETAILS_MODAL_OPEN, cardId };
  },
};
