import { takeLatest, put } from "redux-saga/effects";
import operations from "./operations";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";

function* authUserResponseSideEffects(action) {
  yield put(operations.setAuthUser({ data: action.data }));
  yield put(
    apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
      data: { userId: action.data.userId },
    })
  );
}

function* watchWhoAmISuccess() {
  yield takeLatest(
    apiReduxApps.WHO_AM_I.types.SUCCESS,
    authUserResponseSideEffects
  );
}

function* watchLogoutSuccess() {
  yield takeLatest(
    apiReduxApps.LOGOUT.types.SUCCESS,
    authUserResponseSideEffects
  );
}

function* watchApiAuthenticateWithOneTimeTokenSuccess() {
  yield takeLatest(
    apiReduxApps.AUTHENTICATE_WITH_ONE_TIME_TOKEN.types.SUCCESS,
    authUserResponseSideEffects
  );
}

export default [
  watchWhoAmISuccess(),
  watchLogoutSuccess(),
  watchApiAuthenticateWithOneTimeTokenSuccess(),
];
