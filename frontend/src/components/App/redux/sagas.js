import { takeLatest, put, takeEvery } from "redux-saga/effects";
import operations from "./operations";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { COMPLETE } from "../../../constants";

function* authUserResponseSideEffects(action) {
  yield put(operations.setAuthUser({ data: action.responseData }));
  yield put(
    apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
      data: { userId: parseInt(action.responseData.userId) },
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

/*There are a few actions that can result in a card moving into the "complete" column
when this happens we want to unblock any blocked cards.
*/
function* cardStateChangeSideEffects(action) {
  const card = action.responseData;
  if (card.status === COMPLETE) {
    // check that blocked cards are now unblocked
    if (card.requiredByCards.length) {
      yield put(
        apiReduxApps.FETCH_AGILE_CARDS_THAT_REQUIRE_CARD.operations.start({
          data: { requiresCardId: card.id, assigneeUserId: card.assignees[0] },
        })
      );
    }
  }

  yield;
}

function* watchCardStateChange() {
  yield takeEvery(
    apiReduxApps.CARD_ADD_REVIEW.types.SUCCESS,
    cardStateChangeSideEffects
  );

  yield takeEvery(
    apiReduxApps.CARD_FINISH_TOPIC.types.SUCCESS,
    cardStateChangeSideEffects
  );
}

export default [
  watchWhoAmISuccess(),
  watchLogoutSuccess(),
  watchApiAuthenticateWithOneTimeTokenSuccess(),
  watchCardStateChange(),
];
