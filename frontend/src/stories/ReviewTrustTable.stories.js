import React from "react";
import ReviewTrustTable from "../components/regions/UserDetails/ReviewTrustTable/Presentation";

export default {
    title: "Tilde/ReviewTrustTable",
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