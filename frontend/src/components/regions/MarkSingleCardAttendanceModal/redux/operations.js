import Creators from "./actions.js";

export default {
  ...Creators,
  openWorkshopCardAttendanceForm: ({ cardId }) =>
    Creators.setWorkshopAttendanceOpenCardId({ cardId }),

  closeWorkshopCardAttendanceForm: () =>
    Creators.setWorkshopAttendanceOpenCardId({ cardId: null }),
};
