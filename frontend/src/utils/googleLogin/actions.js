import types from "./types";

export default {
  initialiseGoogleAuthStart: () => {
    return { type: types.INITIALISE_GOOGLE_AUTH_START };
  },

  initialiseGoogleAuthSuccess: ({ data }) => {
    return { type: types.INITIALISE_GOOGLE_AUTH_SUCCESS, data };
  },

  initialiseGoogleAuthError: ({ error }) => {
    return { type: types.INITIALISE_GOOGLE_AUTH_ERROR, error };
  },
};
