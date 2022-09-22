import React from "react";
import BurnDownChart from "../components/regions/UserActions/NewUserBurndownStats";

import burnDownData from "./fixtures/burnDownData";
export default {
  title: "Tilde/UserActions/newBurnDownChart",
  component: BurnDownChart,
};
export const Primary = () => <BurnDownChart burnDownSnapshots={burnDownData} />;
