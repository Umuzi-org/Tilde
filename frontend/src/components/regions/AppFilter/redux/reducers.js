import types from "./types";
const INITIAL_STATE = {
  userId: null,
  cohortId: null,
};

const reducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.SET_FILTER_BY_USER_ID:
      return { ...state, userId: action.userId };
    case types.SET_FILTER_BY_COHORT_ID:
      return { ...state, cohortId: action.cohortId };
    default:
      return state;
  }
};

export default reducer;
