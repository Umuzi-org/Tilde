import React from "react";

import { Paper } from '@material-ui/core';

import LinkToUserBoard from "../../widgets/LinkToUserBoard"
import LinkToUserStats from "../../widgets/LinkToUserStats"

export default ({userId,userBoardSelected,userStatsSelected}) => {
    return (

    <Paper>
        <LinkToUserBoard userId={userId} selected={userBoardSelected}/>
        <LinkToUserStats userId={userId} selected={userStatsSelected}/>
    </Paper>

    
    )
}