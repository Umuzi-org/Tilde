import React, { useState, useEffect } from "react";
import FilterByNames from "./FilterByNames";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles((theme) => {
  return {
    filterByNamesContainer: {
      margin: 0,
      width: "100%",
    },
    filterByNamesItem: {
      maxHeight: "90vh",
      overflowY: "scroll",
    },
    filterByNamesContainerHeading: {
      position: "sticky",
      top: -5,
      padding: "10px",
      backgroundColor: theme.palette.background.default,
      zIndex: 2,
    },
    filterByNamesItemBody: {
      padding: "0px 10px",
    },
  };
});

export default function FilterByNamesFilters({
  filterIncludeTags,
  filterExcludeTags,

  filterIncludeFlavours,
  filterExcludeFlavours,

  handleChangeFlavourFilter,
  handleChangeTagFilter,

  allTagNames,
  allFlavours,
  allTeamNames,
  filterIncludeAssigneeTeams,
  handleChangeAssigneeTeamFilter,
}) {
  const classes = useStyles();

  const [searchTerm, setSearchTerm] = useState("");
  const [allFoundFlavours, setAllFoundFlavours] = useState([]);
  const [allFoundTagNames, setAllFoundTagNames] = useState([]);
  const [allFoundTeamNames, setAllFoundTeamNames] = useState([]);

  function handleChangeSearchTerm(e) {
    setSearchTerm(e.target.value);
  }

  useEffect(() => {
    setAllFoundFlavours(() =>
      allFlavours.filter((flavour) =>
        flavour.toLocaleLowerCase().includes(searchTerm)
      )
    );
    setAllFoundTagNames(() =>
      allTagNames.filter((tagName) =>
        tagName.toLocaleLowerCase().includes(searchTerm)
      )
    );
    setAllFoundTeamNames(() =>
      allTeamNames.filter((teamName) =>
        teamName.toLocaleLowerCase().includes(searchTerm)
      )
    );
  }, [searchTerm, allFlavours, allTagNames, allTeamNames]);

  return (
    <Grid className={classes.filterByNamesItem}>
      <Grid className={classes.filterByNamesContainerHeading}>
        <Typography variant="h5">Filters</Typography>
        <TextField
          variant="outlined"
          placeholder="Filters"
          value={searchTerm}
          onChange={handleChangeSearchTerm}
          fullWidth
        />
      </Grid>
      <Grid className={classes.filterByNamesItemBody}>
        <Typography variant="h6">Filter by flavour</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            allNames={searchTerm ? allFoundFlavours : allFlavours}
            filterInclude={filterIncludeFlavours}
            filterExclude={filterExcludeFlavours}
            onChange={handleChangeFlavourFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by tag</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            allNames={searchTerm ? allFoundTagNames : allTagNames}
            filterInclude={filterIncludeTags}
            filterExclude={filterExcludeTags}
            onChange={handleChangeTagFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by assignee team</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            allNames={searchTerm ? allFoundTeamNames : allTeamNames}
            filterInclude={filterIncludeAssigneeTeams}
            filterExclude={[]}
            onChange={handleChangeAssigneeTeamFilter}
          />
        </Paper>
      </Grid>
    </Grid>
  );
}
