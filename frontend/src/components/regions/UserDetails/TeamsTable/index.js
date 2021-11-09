import React from "react";
import Presentation from "./Presentation";

function TeamsTable({ teams, authUser }) {
  const props = {
    teams,
    authUser,
  };
  return <Presentation {...props} />;
}

export default TeamsTable;
