import React from "react";
import { MarkdownRenderer } from "../../widgets/MarkdownRenderer";

import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";

import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";

const urls = [
  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/apis/basics/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/sql-schema-design/content/topics/sql-schema-design/index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/java-specific/collections-and-datastructures/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/apis/basics/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/sql-schema-design/content/topics/sql-schema-design/index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/java-specific/collections-and-datastructures/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/apis/basics/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/sql-schema-design/content/topics/sql-schema-design/index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/java-specific/collections-and-datastructures/_index.md",
  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/apis/basics/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/sql-schema-design/content/topics/sql-schema-design/index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/java-specific/collections-and-datastructures/_index.md",
  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/apis/basics/_index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/sql-schema-design/content/topics/sql-schema-design/index.md",

  "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/topics/java-specific/collections-and-datastructures/_index.md",
];

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    width: "100%",
    backgroundColor: theme.palette.background.paper,
  },

  button: {
    width: "40px",
  },
}));

const a11yProps = (index) => {
  return {
    id: `scrollable-auto-tab-${index}`,
    "aria-controls": `scrollable-auto-tabpanel-${index}`,
  };
};

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`scrollable-auto-tabpanel-${index}`}
      aria-labelledby={`scrollable-auto-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
};

export default () => {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  return (
    <div className={classes.root}>
      <AppBar position="static" color="default">
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
          variant="scrollable"
          scrollButtons="auto"
          aria-label="scrollable auto tabs example"
        >
          {urls.map((url, index) => {
            return (
              <Tab
                label={
                  <div>
                    Something meaningful {index}
                    <IconButton className={classes.button}>
                      <CloseIcon />
                    </IconButton>
                  </div>
                }
                {...a11yProps(index)}
              />
            );
          })}
        </Tabs>
      </AppBar>

      {urls.map((url, index) => {
        return (
          <TabPanel value={value} index={index} key={index}>
            <MarkdownRenderer src={url} />
          </TabPanel>
        );
      })}
    </div>
  );
};
