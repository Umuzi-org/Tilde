import { all } from "redux-saga/effects";

import { authSagas as googleSagas } from "../utils/googleLogin";

import { apiReduxWatchers } from "../apiAccess/redux/apiApps";
import { appSagas } from "../components/App/redux";
import { recruitAgileBoardSagas } from "../components/regions/RecruitAgileBoard/redux";
import { appFilterSagas } from "../components/regions/AppFilter/redux";
import { cardDetailsModalSagas } from "../components/regions/CardDetailsModal/redux";

import { addCardReviewSagas } from "../components/regions/AddCardReviewModal/redux";

import { projectReportSagas } from "../components/regions/Dashboard/ProjectReport/redux";

// import { markSingleCardWorkshopAttendanceSagas } from "../components/regions/MarkSingleCardAttendanceModal/redux";

import { entitiesSagas } from "../apiAccess/redux";

export function* rootSaga() {
  yield all([
    ...googleSagas,
    ...apiReduxWatchers,
    ...entitiesSagas,
    ...appSagas,
    ...recruitAgileBoardSagas,
    ...cardDetailsModalSagas,
    ...addCardReviewSagas,
    // ...markSingleCardWorkshopAttendanceSagas,
    ...appFilterSagas,
    ...projectReportSagas,
  ]);
}
