import types from "./types.js";

export default {
  setAuthUser: ({ data }) => {
    return { type: types.SET_CURRENT_USER_AUTH_IDENTITY, data };
  },
};
