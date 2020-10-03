import createSagaMiddleware from "redux-saga";
import { rootSaga } from "./sagas";
import googleLogin from "./../utils/googleLogin";

import App from "../components/App/redux";
import AgileBoard from "../components/regions/AgileBoard/redux";
import AppFilter from "../components/regions/AppFilter/redux";
import CardDetailsModal from "../components/regions/CardDetailsModal/redux";

import AddCardReviewModal from "../components/regions/AddCardReviewModal/redux";
import MarkSingleCardAttendanceModal from "../components/regions/MarkSingleCardAttendanceModal/redux";

import ProjectReport from "../components/regions/Dashboard/ProjectReport/redux";

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
    AppFilter,
    CardDetailsModal,
    AddCardReviewModal,
    MarkSingleCardAttendanceModal,
    Entities,
    ProjectReport,
    ...apiReduxReducers,
  }),
  applyMiddleware(logger, sagaMiddleware)
);

sagaMiddleware.run(rootSaga);
