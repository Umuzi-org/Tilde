import { takeEvery, put, select } from "redux-saga/effects";
// import operations from "./operations";
import { apiReduxApps } from "../../../../apiAccess/redux/apiApps";

function* setProjectLinkSuccessSideEffects(action) {
  const { cardId } = action.requestData;

  const getCard = (state) => state.Entities.cards[cardId];

  const card = yield select(getCard);

  const projectId = card.recruitProject;

  yield put(
    apiReduxApps.FETCH_SINGLE_RECRUIT_PROJECT.operations.start({
      data: { projectId },
    })
  );
}

function* watchSetProjectLinkSuccess() {
  yield takeEvery(
    apiReduxApps.CARD_SET_PROJECT_LINK.types.SUCCESS,
    setProjectLinkSuccessSideEffects
  );
}

export default [watchSetProjectLinkSuccess()];
