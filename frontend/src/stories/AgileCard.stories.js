import React from "react";
import Card from "../components/regions/AgileBoard/AgileCard/Presentation";
import card from "./fixtures/agileCard.json";
import user from "./fixtures/user.json";

export default {
    title: "Tilde/AgileCard",
    component: Card
}

const Template = (args) => <Card {...args} />;
export const Primary = Template.bind({});
Primary.args = {
    card,
    authUser,
}