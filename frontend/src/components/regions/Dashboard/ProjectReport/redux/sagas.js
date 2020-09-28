import { takeEvery, put, select } from "redux-saga/effects";
import { appFilterTypes } from "../../../AppFilter/redux";
import { apiReduxApps } from "../../../../../apiAccess/redux/apiApps";

function* setFilterCohortIdSideEffects(action) {
  const userIds = yield select(
    (state) => state.Entities.cohorts[action.cohortId].cohortRecruitUsers
  );

  const dataSequence = userIds.map((userId) => {
    return {
      assigneeUserId: userId,
      page: 1,
    };
  });

  yield put(
    apiReduxApps.FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE.operations.maybeStartCallSequence(
      { dataSequence }
    )
  );
}

function* watchSetFilterCohortId() {
  yield takeEvery(
    appFilterTypes.SET_FILTER_BY_COHORT_ID,
    setFilterCohortIdSideEffects
  );
}

export default [watchSetFilterCohortId()];
