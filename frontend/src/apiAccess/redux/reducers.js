import types from "./types";

const INITIAL_STATE = {};

const reducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.ADD_API_PAGED_OBJECTS_TO_STORE:
      const allInstances = state[action.objectType]
        ? { ...state[action.objectType], ...action.data }
        : action.data;

      return {
        ...state,
        [action.objectType]: allInstances,
      };

    default:
      return state;
  }
};

export default reducer;
