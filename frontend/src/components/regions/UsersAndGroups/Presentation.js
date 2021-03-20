import React from "react";
import { makeStyles } from "@material-ui/core/styles";

// hactoberfest: Visual debt. Make this look better: max height of container should fit viewport
import { Link } from "react-router-dom";

import LinkToUserBoard from "../../widgets/LinkToUserBoard";

import {
  TableRow,
  TableHead,
  TextField,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  Button,
  Typography,
  Tooltip,
} from "@material-ui/core";

import { routes } from "../../../routes";

const useStyles = makeStyles((theme) => ({
  highlightedGroup: {
    backgroundColor: theme.palette.primary.light,
  },
  // container: {
  //   maxHeight: 800,
  // },
  groupName: {
    cursor: "pointer",
  },
}));

export default function Presentation({
  teams,
  users,
  filterByGroup,
  filterByUser,

  filterUsersByGroupName,
  handleUserGroupClick,
}) {
  const classes = useStyles();
  //   const usersLabel = filterUsersByGroupName ? "": "Users"
  return (
    <Grid container>
      <Grid item xs={6} className={classes.grid}>
        <TableContainer className={classes.container}>
          <Table stickyHeader size="small">
            <TableHead>
              <TableRow>
                <TableCell>
                  <TextField
                    label="Teams"
                    variant="outlined"
                    {...filterByGroup}
                  />
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {teams.map((group) => {
                return (
                  <TableRow
                    key={group.id}
                    className={
                      group.name === filterUsersByGroupName
                        ? classes.highlightedGroup
                        : ""
                    }
                  >
                    <Tooltip title="click on the group name to filter users. Click again to cancel the filter">
                      <TableCell
                        onClick={() => handleUserGroupClick(group.name)}
                        className={classes.groupName}
                      >
                        <Typography>{group.name}</Typography>
                      </TableCell>
                    </Tooltip>
                    <TableCell>
                      <Link
                        to={routes.groupCardSummary.route.path.replace(
                          ":teamId",
                          group.id
                        )}
                      >
                        <Button size="small" variant="outlined">
                          Cards
                        </Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>

      <Grid item xs={6} className={classes.grid}>
        <TableContainer className={classes.container}>
          <Table stickyHeader size="small">
            <TableHead>
              <TableRow>
                <TableCell>
                  <TextField
                    label={`${filterUsersByGroupName} Users`}
                    variant="outlined"
                    {...filterByUser}
                  />
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.keys(users)
                .sort()
                .map((email) => {
                  return (
                    <TableRow key={email}>
                      <TableCell>{email}</TableCell>
                      <TableCell>
                        <LinkToUserBoard
                          userId={users[email].userId}
                          label="Details"
                        />
                      </TableCell>
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </Grid>
  );
}
