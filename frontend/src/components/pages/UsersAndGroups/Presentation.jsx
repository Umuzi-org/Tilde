import React from "react";
import { getAgeString } from "../../widgets/utils";
import { getPrStatus, getTildeReviewStatus } from "./utils";
import { makeStyles } from "@material-ui/core/styles";
import LinkToUserBoard from "../../widgets/LinkToUserBoard";
import Button from "../../widgets/Button";

import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Grid,
  TextField,
} from "@material-ui/core";

import FilterIcon from "@material-ui/icons/Filter"; //TODO better icon. Need to upgrade material ui
import LaunchIcon from "@material-ui/icons/Launch";

import { Link } from "react-router-dom";
import { routes } from "../../../routes";

const useStyles = makeStyles((theme) => ({
  marginsAlignment: {
    marginTop: "8px",
    marginLeft: "16px",
  },
  textBoxSize: {
    width: "62%",
  },
  warning: {
    color: theme.palette.warning.dark,
  },
  error: {
    color: theme.palette.error.dark,
  },
  default: {
    color: theme.palette.primary,
  },
  bottomMargin: {
    marginBottom: "8px",
  },
  cards: {
    maxHeight: "90vh",
    padding: "0px 10px",
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  filterCards: {
    position: "sticky",
    top: -5,
    padding: "10px 0px",
    zIndex: 2,
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  ButtonSpaces: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
}));

function TeamSummaryStats({ summaryStats }) {
  const dateOfOldestPullRequest = summaryStats.oldestOpenPrTime
    ? summaryStats.oldestOpenPrTime.slice(0, 10)
    : undefined;
  const dateOfOldestTildeReviewRequest = summaryStats.oldestCardInReviewTime
    ? summaryStats.oldestCardInReviewTime.slice(0, 10)
    : undefined;
  const classes = useStyles();

  const prStatusClassName = classes[getPrStatus(dateOfOldestPullRequest)];
  const tildeReviewStatusClassName =
    classes[getTildeReviewStatus(dateOfOldestTildeReviewRequest)];

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
          <TableCell className={prStatusClassName}>
            {dateOfOldestPullRequest
              ? getAgeString(dateOfOldestPullRequest)
              : "-"}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Review Cards</TableCell>
          <TableCell>{summaryStats.totalCardsInReview}</TableCell>
          <TableCell className={tildeReviewStatusClassName}>
            {dateOfOldestTildeReviewRequest
              ? getAgeString(dateOfOldestTildeReviewRequest)
              : "-"}
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
}

function TeamCard({
  team,
  summaryStats,
  handleUserGroupClick,
  filterUsersByGroupName,
}) {
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
      <Link
        className={classes.ButtonSpaces}
        to={routes.groupCardSummary.route.path.replace(":teamId", team.id)}
      >
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
}

function UserCard({ email, user }) {
  const classes = useStyles();
  return (
    <Paper variant="outlined" elevation={2} className={classes.ButtonSpaces}>
      <Typography
        variant="h6"
        gutterBottom
        component="div"
        className={classes.marginsAlignment}
      >
        {email}
      </Typography>

      <div className={classes.bottomMargin}>
        <LinkToUserBoard userId={user.userId} label="View" />
      </div>
    </Paper>
  );
}

export default function Presentation({
  teams,
  users,
  teamSummaryStats,

  filterFormValues,
  filterUsersByGroupName,
  handleUserGroupClick,
  handleChangeFilterFormInput,
}) {
  const classes = useStyles();
  return (
    <Grid container spacing={2}>
      <Grid item xs={6} className={classes.cards}>
        <Paper variant="outlined" elevation={2} className={classes.filterCards}>
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
            value={filterFormValues.team}
            className={classes.textBoxSize}
            onChange={handleChangeFilterFormInput("team")}
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
      <Grid item xs={6} className={classes.cards}>
        <Paper variant="outlined" elevation={2} className={classes.filterCards}>
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
            value={filterFormValues.user}
            onChange={handleChangeFilterFormInput("user")}
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
