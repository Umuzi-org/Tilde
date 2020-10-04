import types from "./types";

const INITIAL_STATE = {
  authUser: {},
};

const appReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.SET_CURRENT_USER_AUTH_IDENTITY:
      return { ...state, authUser: action.data };
    default:
      return state;
  }
};

export default appReducer;
