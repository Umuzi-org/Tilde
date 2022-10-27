import React from "react";
import Presentation from "./Presentation";

export default function AgileCardUnconnected({
  card,
  repoUrl,
  authUser,
  viewedUser,
  filterUserId,
}) {
  const props = {
    card,
    repoUrl,
    authUser,
    viewedUser,
    filterUserId,
  };

  return <Presentation {...props} />;
}
