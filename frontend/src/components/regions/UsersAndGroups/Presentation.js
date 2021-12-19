import React from "react";
import LinkToUserBoard from "../../widgets/LinkToUserBoard";
import { makeStyles } from "@material-ui/core/styles";
import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Button,
  Grid,
  TextField,
} from "@material-ui/core";

import FilterIcon from "@material-ui/icons/Filter"; //TODO better icon. Need to upgrade material ui
import LaunchIcon from "@material-ui/icons/Launch";

import { Link } from "react-router-dom";
import { routes } from "../../../routes";
const useStyles = makeStyles({
  marginsAlignment: {
    marginTop: "8px",
    marginLeft: "16px",
  },
  textBoxSize: {
    width: "62%",
  },
});
const TeamSummaryStats = ({ summaryStats }) => {
  const oldestOpenPrTime = summaryStats.oldestOpenPrTime
    ? new Date(summaryStats.oldestOpenPrTime)
    : null;

  const oldestCardInReviewTime = summaryStats.oldestCardInReviewTime
    ? new Date(summaryStats.oldestCardInReviewTime)
    : null;

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell></TableCell>
          <TableCell>Count</TableCell>
          <TableCell>Oldest</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        <TableRow>
          <TableCell>Pull Requests</TableCell>
          <TableCell>{summaryStats.totalOpenPrs}</TableCell>
          <TableCell>
            {oldestOpenPrTime ? oldestOpenPrTime.toLocaleString() : "-"}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Review Cards</TableCell>
          <TableCell>{summaryStats.totalCardsInReview}</TableCell>
          <TableCell>
            {oldestCardInReviewTime
              ? oldestCardInReviewTime.toLocaleString()
              : "-"}
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
};

const TeamCard = ({
  team,
  summaryStats,
  handleUserGroupClick,
  filterUsersByGroupName,
}) => {
  const filterButtonVariant =
    team.name === filterUsersByGroupName ? "contained" : "outlined";

  const classes = useStyles();
  return (
    <Paper variant="outlined" elevation={2}>
      <Typography
        variant="h6"
        gutterBottom
        component="div"
        className={classes.marginsAlignment}
      >
        {team.name}
      </Typography>
      <Link to={routes.groupCardSummary.route.path.replace(":teamId", team.id)}>
        <Button
          variant="outlined"
          color="default"
          size="small"
          startIcon={<LaunchIcon />}
          className={classes.marginsAlignment}
        >
          View
        </Button>
      </Link>
      <Button
        variant={filterButtonVariant}
        color="default"
        size="small"
        startIcon={<FilterIcon />}
        onClick={() => handleUserGroupClick(team.name)}
        className={classes.marginsAlignment}
      >
        Filter
      </Button>
      {summaryStats ? <TeamSummaryStats summaryStats={summaryStats} /> : ""}
    </Paper>
  );
};

const UserCard = ({ email, user }) => {
  const classes = useStyles();
  return (
    <Paper variant="outlined" elevation={2}>
      <Typography
        variant="h6"
        gutterBottom
        component="div"
        className={classes.marginsAlignment}
      >
        {email}
      </Typography>

      <LinkToUserBoard
        userId={user.userId}
        className={classes.title}
        label="View"
      />
    </Paper>
  );
};

export default function Presentation({
  teams,
  users,
  teamSummaryStats,
  filterByGroup,
  filterByUser,

  filterUsersByGroupName,
  handleUserGroupClick,
}) {
  const classes = useStyles();
  return (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <Paper variant="outlined" elevation={2}>
          <Typography
            variant="h5"
            gutterBottom
            component="div"
            className={classes.marginsAlignment}
          >
            Teams
          </Typography>

          <TextField
            label="Teams"
            variant="outlined"
            {...filterByGroup}
            className={classes.textBoxSize}
          />
        </Paper>
        {teams.map((team) => {
          return (
            <TeamCard
              key={team.id}
              team={team}
              summaryStats={teamSummaryStats[team.id]}
              handleUserGroupClick={handleUserGroupClick}
              filterUsersByGroupName={filterUsersByGroupName}
            />
          );
        })}
      </Grid>
      <Grid item xs={6}>
        <Paper variant="outlined" elevation={2}>
          <Typography
            variant="h5"
            gutterBottom
            component="div"
            className={classes.marginsAlignment}
          >
            Users
          </Typography>
          <TextField
            label={`${filterUsersByGroupName} Users`}
            variant="outlined"
            {...filterByUser}
            className={classes.textBoxSize}
          />
        </Paper>
        {Object.keys(users)
          .sort()
          .map((email) => {
            return <UserCard key={email} email={email} user={users[email]} />;
          })}
      </Grid>
    </Grid>
  );
}
