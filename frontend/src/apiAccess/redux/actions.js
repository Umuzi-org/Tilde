import types from "./types.js";

export default {
  addEntitiesToStoreAsObject: ({ data, objectType }) => {
    return { type: types.ADD_API_PAGED_OBJECTS_TO_STORE, data, objectType };
  },
};
