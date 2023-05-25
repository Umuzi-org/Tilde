import React from "react";
import ReviewTrustTable from "../components/pages/UserDashboard/UserDetails/ReviewTrustTable/Presentation";

export default {
    title: "Tilde/pages/UserDashboard/ReviewTrustTable",
    component: ReviewTrustTable
}

const trustInstances = [
    {
        content_item_title: "Title 1",
        flavours: ["javascript","react"] 
    }, 
    {
        content_item_title: "Title 2",
        flavours: ["python","pytest"] 
    }, 
]
    
export const Primary = () => <ReviewTrustTable trustInstances={trustInstances}/>