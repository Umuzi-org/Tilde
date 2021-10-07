import Creators from "./actions.js";

export default {
    ...Creators,
    openTeamsTable: ({ userId }) =>
        Creators.setTeamsTableOpen({ userId }),
    closeTeamsTable: () =>
        Creators.setTeamsTableOpen({ userId: null }),
};