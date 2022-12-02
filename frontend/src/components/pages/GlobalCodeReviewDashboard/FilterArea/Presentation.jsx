import React from "react";
import FilterByNames from "../FilterByNames";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/styles";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles((theme) => {
  return {
    filterByItemNames: {
      maxHeight: "90vh",
      overflowY: "scroll",
    },
    filterByContainerHeadingNames: {
      position: "sticky",
      top: -5,
      padding: "10px",
      backgroundColor: "#fff",
      zIndex: 2,
    },
    filterByItemBodyNames: {
      padding: "0px 10px",
    },
  };
});

export default function Presentation({
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

  cardNameSearchValue,
  handleChangeCardNameSearchValue,
}) {
  const classes = useStyles();

  return (
    <Grid className={classes.filterByItemNames}>
      <Grid className={classes.filterByContainerHeadingNames}>
        <Typography variant="h5">Filters</Typography>
      </Grid>
      <Grid className={classes.filterByItemBodyNames}>
        <Typography variant="h6">Filter by flavour</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            allNames={allFlavours}
            filterInclude={filterIncludeFlavours}
            filterExclude={filterExcludeFlavours}
            onChange={handleChangeFlavourFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by tag</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            allNames={allTagNames}
            filterInclude={filterIncludeTags}
            filterExclude={filterExcludeTags}
            onChange={handleChangeTagFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by assignee team</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            allNames={allTeamNames}
            filterInclude={filterIncludeAssigneeTeams}
            filterExclude={[]}
            onChange={handleChangeAssigneeTeamFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by card name</Typography>
        <Paper>
          <TextField
            variant="outlined"
            placeholder="Card name"
            value={cardNameSearchValue}
            onChange={handleChangeCardNameSearchValue}
            fullWidth
          />
        </Paper>
      </Grid>
    </Grid>
  );
}
