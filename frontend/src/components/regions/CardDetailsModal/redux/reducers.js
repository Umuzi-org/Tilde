import types from "./types";
const INITIAL_STATE = {
  cardId: null,
};
const reducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.SET_CARD_DETAILS_MODAL_OPEN:
      return { ...state, cardId: action.cardId };
    default:
      return state;
  }
};
export default reducer;
