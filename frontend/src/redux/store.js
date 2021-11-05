import createSagaMiddleware from "redux-saga";
import { rootSaga } from "./sagas";
import googleLogin from "./../utils/googleLogin";

import App from "../components/App/redux";
import AgileBoard from "../components/regions/AgileBoard/redux";
import CardDetails from "../components/regions/CardDetails/redux";

import AddCardReviewModal from "../components/regions/AddCardReviewModal/redux";
import MarkSingleCardAttendanceModal from "../components/regions/MarkSingleCardAttendanceModal/redux";

import Entities from "../apiAccess/redux";

import { applyMiddleware, combineReducers, createStore } from "redux";

import { apiReduxReducers } from "../apiAccess/redux/apiApps";

// Logger with default options
import logger from "redux-logger";
// see https://github.com/LogRocket/redux-logger
// import { appSagas } from "../components/App/redux";

const sagaMiddleware = createSagaMiddleware();

// window.apiReduxReducers = apiReduxReducers;

export const store = createStore(
  combineReducers({
    App,
    AgileBoard,
    googleLogin,
    CardDetails,
    AddCardReviewModal,
    MarkSingleCardAttendanceModal,
    Entities,
    ...apiReduxReducers,
  }),
  applyMiddleware(logger, sagaMiddleware)
);

sagaMiddleware.run(rootSaga);
