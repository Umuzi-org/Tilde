import React from "react";
import BurnDownChart from "../components/pages/UserDashboard/BurnDownChart/Presentation";
import burnDownData from "./fixtures/burnDownData";
export default {
    title: "Tilde/pages/UserDashboard/BurnDownChart",
    component: BurnDownChart,
}
export const Primary = () => <BurnDownChart burnDownSnapshots={burnDownData}/>