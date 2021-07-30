import Creators from "./actions.js";

export default {
    ...Creators,
    openDueTimeFormModal: ({ cardId }) =>
    Creators.setDueTimeFormModalOpen({ cardId }),
    closeDueTimeFormModal: () =>
    Creators.setDueTimeFormModalOpen({ cardId: null }),
};