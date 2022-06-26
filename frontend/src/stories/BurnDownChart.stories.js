import React from "react";
import BurnDownChart from "../components/regions/BurnDownChart/Presentation";
import burnDownData from "./fixtures/burnDownData";
export default {
    title: "Tilde/BurnDownChart",
    component: BurnDownChart,
}
export const Primary = () => <BurnDownChart burnDownSnapshots={burnDownData}/>