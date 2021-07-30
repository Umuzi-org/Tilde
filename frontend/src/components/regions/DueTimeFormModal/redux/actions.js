import types from "./types.js";

export default {
  setDueTimeFormModalOpen: ({ cardId }) => {
    return { type: types.SET_DUE_TIME_FORM_MODAL_OPEN, cardId };
  },
};