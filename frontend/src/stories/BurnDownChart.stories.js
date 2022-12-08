import React from "react";
import BurnDownChart from "../components/pages/UserActions/UserBurndownStats";

import burnDownData from "./fixtures/burnDownData";
export default {
  title: "Tilde/UserActions/BurnDownChart",
  component: BurnDownChart,
};
export const Primary = () => <BurnDownChart burnDownSnapshots={burnDownData} />;
