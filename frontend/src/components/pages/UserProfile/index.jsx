import React from "react";
import Presentation from "./Presentation";

export default ({ nameTag }) => {
  let nameTag = "some name";

  const props = {
    nameTag,
  };

  return <Presentation {...prop} />;
};
