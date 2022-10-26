import React from "react";
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Switch from "@material-ui/core/Switch";
import TextField from "@material-ui/core/TextField";
export default function FilterByNames({
  allNames,
  filterInclude,
  filterExclude,
  onChange,
  searchTerm,
  handleChangeSearchTerm,
  groupName,
}) {
  allNames = allNames || [];
  filterInclude = filterInclude || [];
  filterExclude = filterExclude || [];
  const allFilters = [...filterInclude, ...filterExclude];

  return (
    <React.Fragment>
      <TextField
        variant="outlined"
        placeholder={groupName}
        value={searchTerm}
        onChange={handleChangeSearchTerm}
        groupName={groupName}
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
