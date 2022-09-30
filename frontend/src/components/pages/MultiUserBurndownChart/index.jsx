import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { apiReduxApps } from "../../../apiAccess/apiApps";

export function MultiUserBurndownChartUnconnected({
  //   mapStateToProps

  // mapDispatchToProps

  // storybook
  forceUser,
}) {}

const mapStateToProps = (state) => {};

const mapDispatchToProps = (dispatch) => {};

const MultiUserBurndownChart = connect(
  mapStateToProps,
  mapDispatchToProps
)(MultiUserBurndownChartUnconnected);
export default MultiUserBurndownChart;
