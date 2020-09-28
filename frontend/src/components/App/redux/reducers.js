import types from "./types";

const INITIAL_STATE = {
  authUser: {},
  //   appFilter: {
  //     userId: null,
  //   },
};

const appReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.SET_CURRENT_USER_AUTH_IDENTITY:
      return { ...state, authUser: action.data };
    // case types.SET_SELECTED_USER:
    //   return {
    //     ...state,
    //     appFilter: { ...state.appFilter, userId: action.userId },
    //   };
    default:
      return state;
  }
};

export default appReducer;
