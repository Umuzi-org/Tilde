import types from "./types";
const INITIAL_STATE = {
  responseData: false,
  loading: false,
  error: "",
};
const reducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case types.INITIALISE_GOOGLE_AUTH_START:
      return { ...state, loading: true };

    case types.INITIALISE_GOOGLE_AUTH_SUCCESS:
      return { ...state, responseData: action.data, error: "" };

    case types.INITIALISE_GOOGLE_AUTH_ERROR:
      return { ...state, error: action.error };

    default:
      return state;
  }
};

export default reducer;
