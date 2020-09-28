import { takeEvery, put } from "redux-saga/effects";
import { appFilterTypes } from "../../AppFilter/redux";

import { apiReduxApps } from "../../../../apiAccess/redux/apiApps";

import constants from "../../../../constants";

function* setFilterUserIdSideEffects(action) {
  const dataSequence1 = Object.keys(constants.AGILE_CARD_STATUS_CHOICES).map(
    (status) => {
      return {
        page: 1,
        assigneeUserId: action.userId,
        status,
      };
    }
  );
  const dataSequence2 = Object.keys(constants.AGILE_CARD_STATUS_CHOICES).map(
    (status) => {
      return {
        page: 1,
        reviewerUserId: action.userId,
        status,
      };
    }
  );

  const dataSequence = [dataSequence1, dataSequence2].flat();

  //   throw new Error(JSON.stringify(dataSequence));

  yield put(
    apiReduxApps.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE.operations.maybeStartCallSequence(
      { dataSequence }
    )
  );

  //   yield put(
  //     apiReduxApps.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE.operations.maybeStartCallSequence(
  //       { dataSequence: dataSequence2 }
  //     )
  //   );
}

function* watchSetFilterUserId() {
  yield takeEvery(
    appFilterTypes.SET_FILTER_BY_USER_ID,
    setFilterUserIdSideEffects
  );
}

export default [watchSetFilterUserId()];
