import React from 'react';
import Presentation from "./Presentation"
import { useParams } from "react-router-dom";

export default ({}) =>{
    let urlParams = useParams() || {};

    const props = {
        userId:urlParams.userId ,
        userBoardSelected: true,
        userStatsSelected: false
        
    }
    return <Presentation {...props}/>
}