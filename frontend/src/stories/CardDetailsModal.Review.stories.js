import React from "react";
import Review  from "../components/regions/CardDetailsModal/Review";
import review from "./fixtures/review.json";

export default {
    title: "Tilde/CardDetailsModal/SingleReview",
    component: Review,
}

const Template = (args) => <Review {...args} />
export const Primary = Template.bind({})
Primary.args = {
    review,
}