import React from "react";
import AgileCardActions from "../components/regions/AgileBoard/AgileCard/AgileCardActions/Presentation";
import card from "../stories/fixtures/agileCard.json";
import user from "../stories/fixtures/user.json";

export default {
    title: "Tilde/AgileCardActions",
    component: AgileCardActions,
}

const Template = (args) => <AgileCardActions {...args} />;
export const AgileCardAction = Template.bind({});
AgileCardAction.args = {
    card,
};