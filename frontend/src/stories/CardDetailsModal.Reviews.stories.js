import React from 'react';

import Reviews from "../components/regions/CardDetailsModal/Reviews"

import reviewObject from "./assets/review.json"

export default {
    title: 'Tilde/CardDetailsModal/Reviews',
    component: Reviews,
    argTypes: {
    //   backgroundColor: { control: 'color' },
    },
  };


  const Template = (args) => <Reviews {...args} />;
  export const Loading = Template.bind({});
  Loading.args = {
    reviewIds: [123],
    reviews : []
}
  export const Primary = Template.bind({});
  Primary.args = {
      reviewIds: [4857],
      reviews: [

        {"id":4857,"status":"NYC","timestamp":"2020-10-29T03:47:20.636784Z","comments":"This is good work! There are "},
        reviewObject,
{"id":4857,"status":"NYC","timestamp":"2020-10-29T03:47:20.636784Z","comments":"This is good work! There are "},
      ]
  };