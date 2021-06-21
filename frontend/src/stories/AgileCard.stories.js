import React from "react";
import Card from "../components/regions/AgileBoard/AgileCard/Presentation"; //List
import AgileCardActions from "../components/regions/AgileBoard/AgileCard/AgileCardActions/Presentation"; //ListItem

import { AgileCardAction } from "../stories/AgileCardActions.stories";

import card from "./fixtures/agileCard.json";
import user from "./fixtures/user.json";

export default {
    title: "Tilde/AgileCard",
    component: Card
}

const Template = ({ items, ...args }) => (
    <Card>
      {items.map((item) => (
        <AgileCardActions {...item} />
      ))}
    </Card>
);
  
export const Primary = Template.bind({});
Primary.args = { 
    items: [AgileCardAction.args]
};