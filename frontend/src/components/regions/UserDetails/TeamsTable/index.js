import React from "react";
import Presentation from "./Presentation";

function TeamsTable({ teams }) {
  const props = {
    teams,
  };
  return <Presentation {...props} />;
}

export default TeamsTable;
