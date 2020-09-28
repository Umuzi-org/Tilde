import Creators from "./actions.js";

const arrayToObjectWithIdKeys = ({ data }) => {
  let dataAsObject = {};

  data.forEach((element) => {
    dataAsObject[element.id] = element;
  });
  return dataAsObject;
};

const addEntityListToStore = ({ data, objectType }) => {
  return Creators.addEntitiesToStoreAsObject({
    data: arrayToObjectWithIdKeys({ data }),
    objectType,
  });
};

export default {
  ...Creators,
  addEntityListToStore,
};
