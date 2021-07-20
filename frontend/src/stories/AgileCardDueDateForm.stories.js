import React from "react";
import AgileCardDueDateForm from "../components/regions/AgileCardDueDateForm/Presentation";

import agileCard from "./fixtures/agileCard.json";

export default {
    title: "Tilde/AgileCardDueDateForm",
    component: AgileCardDueDateForm
}

export const Primary = () => <AgileCardDueDateForm dueTime={agileCard.dueTime}/>