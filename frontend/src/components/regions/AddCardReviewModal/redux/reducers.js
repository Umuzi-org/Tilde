import types from "./types";
const INITIAL_STATE = {
  cardId: null,
};
const reducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.SET_PROJECT_REVIEW_OPEN_CARD_ID:
      return { ...state, cardId: action.cardId };
    default:
      return state;
  }
};
export default reducer;
