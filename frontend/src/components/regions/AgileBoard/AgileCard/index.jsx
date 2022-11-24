import React from "react";
import Presentation from "./Presentation";

export default function AgileCardUnconnected({
  card,
  authUser,
  viewedUser,
  filterUserId,
}) {
  const props = {
    card,
    authUser,
    viewedUser,
    filterUserId,
  };

  return <Presentation {...props} />;
}
