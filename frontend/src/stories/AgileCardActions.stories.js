import React from "react";
import AgileCardActions from "../components/regions/AgileBoard/AgileCard/AgileCardActions/Presentation.jsx";
import card from "../stories/fixtures/AgileCards/openPrCard.json";

export default {
  title: "Tilde/AgileCardActions",
  component: AgileCardActions,
};

const Template = (args) => <AgileCardActions {...args} />;
export const Primary = Template.bind({});
Primary.args = {
  card,
};
