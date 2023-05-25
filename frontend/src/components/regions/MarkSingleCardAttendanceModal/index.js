import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import operations from "./redux/operations.js";
import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

const MarkSingleCardAttendanceModalUnconnected = ({
  card,
  saveWorkshopAttendance,
  closeModal,
}) => {
  const [
    formState,
    { date, time },
    formErrors,
    dataFromState,
  ] = useMaterialUiFormState({
    date: {
      required: true,
      default: new Date("2014-08-18T21:11:54"),
    },
    time: {
      required: false,
      default: new Date("2014-08-18T21:11:54"),
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const { date, time } = dataFromState({ state: formState });
    saveWorkshopAttendance({ date, time, cardId: card.id });
  };

  const props = {
    card,
    date,
    time,
    handleSubmit,
    formErrors,
    closeModal,
  };

  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  const cardId = state.MarkSingleCardAttendanceModal.cardId;
  const card =
    !!cardId & (state.apiEntities.cards !== undefined)
      ? state.apiEntities.cards[cardId]
      : null;

  return {
    card,
  };
};
const mapDispatchToProps = (dispatch) => {
  return {
    closeModal: () => {
      dispatch(operations.closeWorkshopCardAttendanceForm());
    },

    saveWorkshopAttendance: ({ cardId, date, time }) => {
      dispatch(
        apiReduxApps.CARD_ADD_WORKSHOP_ATTENDANCE.operations.start({
          data: cardId,
          date,
          time,
        })
      );
    },
  };
};
const MarkSingleCardAttendanceModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(MarkSingleCardAttendanceModalUnconnected);

export default MarkSingleCardAttendanceModal;
