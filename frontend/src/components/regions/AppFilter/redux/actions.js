import types from "./types.js";

export default {
  setFilterByUserId: ({ userId }) => {
    return { type: types.SET_FILTER_BY_USER_ID, userId };
  },

  setFilterByCohortId: ({ cohortId }) => {
    return { type: types.SET_FILTER_BY_COHORT_ID, cohortId };
  },
};
