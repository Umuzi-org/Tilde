import React from "react";
import Button from "@material-ui/core/Button";
import LaunchIcon from "@material-ui/icons/Launch";
// import { makeStyles } from "@material-ui/core/styles";

// const useStyles = makeStyles((theme) => {
//   return {
//     button: {},
//   };
// });

function getViewUrl({ contentUrl }) {
  let urlEnd = contentUrl.slice(
    contentUrl.search("/content/") + "/content/".length
  );
  // 'projects/nodejs/sql/_index.md'
  urlEnd = urlEnd.slice(0, urlEnd.length - "/index.md".length);
  // 'projects/nodejs/sql/'
  return `https://umuzi-org.github.io/tech-department/${urlEnd}`;
}

export default ({ contentItemId, contentUrl, className }) => {
  //   const classes = useStyles();

  if (contentUrl === undefined) return <React.Fragment />;

  return (
    <a
      href={getViewUrl({ contentUrl })}
      target="_blank"
      rel="noopener noreferrer"
    >
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
