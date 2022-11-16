import React from "react";
import DueTimeFormModal from "../components/regions/DueTimeFormModal/Presentation";

import agileCard from "./fixtures/agileCard.json";

export default {
  title: "Tilde/DueTimeFormModal",
  component: DueTimeFormModal,
};

export const Primary = () => (
  <DueTimeFormModal
    cards={agileCard}
    cardId={agileCard.id}
    handleSubmit={() => {}}
  />
);
