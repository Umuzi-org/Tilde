import React from "react";
import Button from "@material-ui/core/Button";

export default ({ className }) => {
  const classes = useStyles();

  return (
    <a href={contentUrl} target="_blank" rel="noopener noreferrer">
      <Button variant="" color="" size="" className={className}>
        {/*  */}
      </Button>
    </a>
  );
};
