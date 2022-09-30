import types from "./types.js";

export default {
  fetchAllPages: ({ API_BASE_TYPE, requestData }) => {
    return { type: types.FETCH_ALL_PAGES_FROM_API, API_BASE_TYPE, requestData };
  },
};
