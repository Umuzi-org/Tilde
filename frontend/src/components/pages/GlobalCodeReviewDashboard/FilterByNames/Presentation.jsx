import React from "react";
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Switch from "@material-ui/core/Switch";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles((theme) => {
  return {
    filtergroupTextbox: {
      marginBottom: theme.spacing(1),
    },
  };
});

export default function Presentation({
  allNames,
  filterExclude,
  onChange,
  searchTerm,
  handleChangeSearchTerm,
  filterGroupName,
  allFilters,
}) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <TextField
        className={classes.filtergroupTextbox}
        variant="outlined"
        placeholder={filterGroupName}
        value={searchTerm}
        onChange={handleChangeSearchTerm}
        fullWidth
      />
      {allNames.map((name, index) => (
        <FormGroup key={`${name}_${index}`}>
          <FormControlLabel
            control={
              <Switch
                size="small"
                color={filterExclude.includes(name) ? "secondary" : "primary"}
                onChange={onChange(name)}
              />
            }
            label={name}
            checked={allFilters.includes(name)}
          />
        </FormGroup>
      ))}
    </React.Fragment>
  );
}
