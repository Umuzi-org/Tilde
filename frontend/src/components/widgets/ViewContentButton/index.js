import React from "react";
import Button from "../Button";
import LaunchIcon from "@material-ui/icons/Launch";

export default ({ contentItemId, contentUrl, className }) => {
  //   const classes = useStyles();

  if (contentUrl === undefined) return <React.Fragment />;

  return (
    <a href={contentUrl} target="_blank" rel="noopener noreferrer">
      <Button
        variant="outlined"
        color="default"
        size="small"
        className={className}
        startIcon={<LaunchIcon />}
      >
        View Content
      </Button>
    </a>
  );
};
