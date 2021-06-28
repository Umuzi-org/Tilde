import React from "react";
import AgileCard from "../components/regions/AgileBoard/AgileCard/Presentation"; 

import agileCard from "./fixtures/agileCard.json";
import user from "./fixtures/user.json";
import authUser from "./fixtures/authUser.json";

export default {
    title: "Tilde/AgileCard",
    component: AgileCard
}

const Template = ({ items, ...args }) => {

    const props = {
      card: agileCard,
      authUser: authUser,
      viewedUser: user,
      filterUserId: user.id,

      handleClickAddReview: () => {},
      handleClickOpenCardDetails: () => {},

      handleRequestReview: () => {},
      handleStartProject: () => {},
      handleCancelReviewRequest: () => {},

      handleClickOpenWorkshopAttendanceForm: () => {},
      handleStartTopic: () => {},
      handleStopTopic: () => {},
      handleFinishTopic: () => {},
      handleRemoveWorkshopAttendance: () => {},

      loadingStartProject: false,
      loadingStartTopic: false,
      loadingClickOpenWorkshopAttendanceForm: false,
      loadingRequestReview: false,
      loadingCancelReviewRequest: false,
      loadingStopTopic: false,
      loadingFinishTopic: false,
      loadingRemoveWorkshopAttendance: false,
    }

    return  <AgileCard {...props} />
};
  
export const Primary = Template.bind({});
Primary.args = { 
    
};