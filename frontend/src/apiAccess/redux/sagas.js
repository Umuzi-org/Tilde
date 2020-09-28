import { pagedApiAppTypes, apiReduxApps, entityApiAppTypes } from "./apiApps";
import { takeEvery, put } from "redux-saga/effects";
import operations from "./operations";

const fetchPageSagas = Object.keys(pagedApiAppTypes).map((BASE_TYPE) => {
  function* successfulFetchSideEffects(action, data) {
    const objectType = pagedApiAppTypes[BASE_TYPE];

    yield put(
      operations.addEntityListToStore({
        data: action.data.results,
        objectType,
      })
    );
  }

  function* watchSucessfulFetch() {
    yield takeEvery(
      apiReduxApps[BASE_TYPE].types.SUCCESS,
      successfulFetchSideEffects
    );
  }
  return watchSucessfulFetch();
});

const fetchSingleEntitySagas = Object.keys(entityApiAppTypes).map(
  (BASE_TYPE) => {
    function* successfulFetchSideEffects(action, data) {
      const objectType = entityApiAppTypes[BASE_TYPE];
      yield put(
        operations.addEntitiesToStoreAsObject({
          data: { [action.data.id]: action.data },
          objectType,
        })
      );
    }

    function* watchSucessfulFetch() {
      yield takeEvery(
        apiReduxApps[BASE_TYPE].types.SUCCESS,
        successfulFetchSideEffects
      );
    }
    return watchSucessfulFetch();
  }
);

function* agileCardClosedSideEffects(action) {
  if (action.data.status === "C") {
    const dataSequence = action.data.requiredByCards.map((cardId) => {
      return { cardId };
    });

    yield put(
      apiReduxApps.FETCH_SINGLE_AGILE_CARD.operations.startCallSequence({
        dataSequence,
      })
    );
  }
}

function* watchAgileCardClosed() {
  yield takeEvery(
    // apiReduxApps.CARD_ADD_WORKSHOP_ATTENDANCE.types.SUCCESS,
    "API_CARD_ADD_WORKSHOP_ATTENDANCE_SUCCESS",
    agileCardClosedSideEffects
  );

  yield takeEvery(
    apiReduxApps.CARD_ADD_REVIEW.types.SUCCESS,
    agileCardClosedSideEffects
  );

  yield takeEvery(
    apiReduxApps.CARD_FINISH_TOPIC.types.SUCCESS,
    agileCardClosedSideEffects
  );
}
export default [
  ...fetchPageSagas,
  ...fetchSingleEntitySagas,
  watchAgileCardClosed(),
];
