import React from "react";
import FilterByNames from "../FilterByNames";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/styles";
import TextField from "@material-ui/core/TextField";
import { filterList } from "../utils";

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
      backgroundColor: "#fff",
      zIndex: 2,
    },
    filterByNamesItemBody: {
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

  handleChangeSearchTerm,
  flavourSearchTerm,
  setFlavourSearchTerm,
  tagSearchTerm,
  setTagSearchTerm,
  assigneeTeamSearchTerm,
  setAssigneeTeamSearchTerm,
}) {
  const classes = useStyles();

  return (
    <Grid className={classes.filterByNamesItem}>
      <Grid className={classes.filterByNamesContainerHeading}>
        <Typography variant="h5">Filters</Typography>
      </Grid>
      <Grid className={classes.filterByNamesItemBody}>
        <Typography variant="h6">Filter by flavour</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            filterGroupName="Flavour"
            handleChangeSearchTerm={(e) =>
              handleChangeSearchTerm({
                e,
                setSearchTermMethod: setFlavourSearchTerm,
              })
            }
            allNames={filterList({
              list: allFlavours,
              filter: flavourSearchTerm,
            })}
            filterInclude={filterIncludeFlavours}
            filterExclude={filterExcludeFlavours}
            onChange={handleChangeFlavourFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by tag</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            filterGroupName="Tag"
            handleChangeSearchTerm={(e) =>
              handleChangeSearchTerm({
                e,
                setSearchTermMethod: setTagSearchTerm,
              })
            }
            allNames={filterList({
              list: allTagNames,
              filter: tagSearchTerm,
            })}
            filterInclude={filterIncludeTags}
            filterExclude={filterExcludeTags}
            onChange={handleChangeTagFilter}
          />
        </Paper>
        <Typography variant="h6">Filter by assignee team</Typography>
        <Paper className={classes.filterByItemPaper}>
          <FilterByNames
            filterGroupName="Assignee team"
            handleChangeSearchTerm={(e) =>
              handleChangeSearchTerm({
                e,
                setSearchTermMethod: setAssigneeTeamSearchTerm,
              })
            }
            allNames={filterList({
              list: allTeamNames,
              filter: assigneeTeamSearchTerm,
            })}
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
