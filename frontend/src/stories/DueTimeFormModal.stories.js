import React from "react";
import DueTimeFormModal from "../components/regions/DueTimeFormModal/Presentation";

import agileCard from "./fixtures/agileCard.json";

export default {
    title: "Tilde/DueTimeFormModal/DueTimeFormModal",
    component: DueTimeFormModal
}

export const Primary = () => <DueTimeFormModal dueTime={agileCard.dueTime}/>