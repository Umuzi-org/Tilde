import createSagaMiddleware from "redux-saga";
import { rootSaga } from "./sagas";
import googleLogin from "./../utils/googleLogin";
import App from "../components/App/redux";
import AgileBoard from "../components/regions/AgileBoard/redux";
import DueTimeFormModal from "../components/regions/DueTimeFormModal/redux";
import CardDetails from "../components/pages/CardDetails";
import AddCardReviewModal from "../components/regions/AddCardReviewModal/redux";
import apiUtilities from "../apiAccess/redux";
import MarkSingleCardAttendanceModal from "../components/regions/MarkSingleCardAttendanceModal/redux";

// import Entities from "../apiAccess/redux";

import { applyMiddleware, combineReducers, createStore, compose } from "redux";

import { apiReduxReducers } from "../apiAccess/apiApps";

// Logger with default options
// import logger from "redux-logger";
// see https://github.com/LogRocket/redux-logger
// import { appSagas } from "../components/App/redux";

import apiEntities from "@prelude/redux-api-toolbox/src/apiEntities";
import utilities from "@prelude/redux-api-toolbox/src/utilities";
import { apiReduxReducers as authReducers } from "@prelude/redux-api-toolbox/src/djRestAuth";
const sagaMiddleware = createSagaMiddleware();

const composeEnhancers =
  (typeof window !== "undefined" &&
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__) ||
  compose;

export const store = createStore(
  combineReducers({
    App,
    AgileBoard,
    googleLogin,
    CardDetails,
    AddCardReviewModal,
    DueTimeFormModal,
    MarkSingleCardAttendanceModal,
    // Entities,
    ...apiReduxReducers,
    utilities,
    apiEntities,
    ...authReducers,

    apiUtilities,
  }),
  // composeEnhancers(applyMiddleware(sagaMiddleware, logger))
  composeEnhancers(applyMiddleware(sagaMiddleware))
);

sagaMiddleware.run(rootSaga);
