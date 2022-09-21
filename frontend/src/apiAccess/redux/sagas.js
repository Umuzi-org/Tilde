import { takeLatest, put, takeEvery, select } from "redux-saga/effects";
import operations from "./operations";
import { apiReduxApps } from "../apiApps";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/appCreator";

import types from "./types";

function* fetchAllPagesSideEffects({ API_BASE_TYPE, requestData }) {
  const callLog = yield select((state) => state[API_BASE_TYPE]);
  const lastCall = getLatestMatchingCall({ callLog, requestData });

  const startPage = requestData.page;
  if (startPage === undefined) throw new Error("page must be defined");

  console.log({ lastCall });

  const { next, count, results } = lastCall.responseData;

  if (next === null) return;
  const pageSize = results.length;

  const maxPage = Math.ceil(count / pageSize);

  const pagesToFetch = [];
  for (let n = startPage + 1; n <= maxPage; n++) pagesToFetch.push(n);

  const dataSequence = pagesToFetch.map((page) => {
    return { ...requestData, page };
  });

  yield put(
    apiReduxApps[API_BASE_TYPE].operations.maybeStartCallSequence({
      dataSequence,
    })
  );
}

function* watchFetchAllPages() {
  yield takeEvery(types.FETCH_ALL_PAGES_FROM_API, fetchAllPagesSideEffects);
}

export default [watchFetchAllPages()];
