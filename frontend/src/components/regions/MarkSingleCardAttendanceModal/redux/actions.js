import types from "./types.js";

export default {
  setWorkshopAttendanceOpenCardId: ({ cardId }) => {
    return { type: types.SET_WORKSHOP_ATTENDANCE_OPEN_CARD_ID, cardId };
  },
};
