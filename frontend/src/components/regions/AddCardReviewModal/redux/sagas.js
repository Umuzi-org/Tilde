import { takeLatest, put, takeEvery, select } from "redux-saga/effects";
import operations from "./operations";
import { apiReduxApps } from "../../../../apiAccess/apiApps";
import types from "./types";

function* addReviewSuccessSideEffects(action) {
  const cardId = action.responseData.id;
  const projectId = action.responseData.recruitProject;

  yield put(operations.closeCardReviewForm());
  yield put(
    apiReduxApps.FETCH_SINGLE_PROJECT_CARD_SUMMARY.operations.start({
      data: { cardId },
    })
  );

  yield put(
    apiReduxApps.FETCH_SINGLE_RECRUIT_PROJECT.operations.start({
      data: { projectId },
    })
  );

  yield put(
    apiReduxApps.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE.operations.start({
      data: {
        projectId,
        page: 1,
      },
    })
  );
}

function* setOpenProjectReviewCardIdSideEffects({ cardId }) {
  if (cardId) {
    const cards = yield select((state) => state.apiEntities.cards) || {};
    const card = cards[cardId];
    if (!card) {
      yield put(
        apiReduxApps.FETCH_SINGLE_AGILE_CARD.operations.start({
          data: {
            cardId,
          },
        })
      );
    }
  }
}

function* watchAddReviewSuccess() {
  yield takeLatest(
    apiReduxApps.CARD_ADD_REVIEW.types.SUCCESS,
    addReviewSuccessSideEffects
  );
}

function* watchSetOpenProjectReviewCardId() {
  yield takeEvery(
    types.SET_PROJECT_REVIEW_OPEN_CARD_ID,
    setOpenProjectReviewCardIdSideEffects
  );
}

export default [watchAddReviewSuccess(), watchSetOpenProjectReviewCardId()];
