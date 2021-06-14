import React from "react";
import CardActions from "../components/regions/AgileBoard/AgileCard/AgileCardActions/Presentation";
import card from "./fixtures/agileCardAction.json";

export default {
    title: "Tilde/AgileCardActions",
    component: CardActions
}

const Template = (args) => <CardActions {...args} />;
export const Primary = Template.bind({});
Primary.args = {
    card,
}