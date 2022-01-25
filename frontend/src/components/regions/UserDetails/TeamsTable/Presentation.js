import React from "react";
import PropTypes from "prop-types";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import { makeStyles } from "@material-ui/core/styles";
import { Typography, Button } from "@material-ui/core";
import { Link } from "react-router-dom";
import { routes } from "../../../../routes";
import LaunchIcon from "@material-ui/icons/Launch";

const useStyles = makeStyles(() => ({
  tableHead: {
    textAlign: "center",
  },
}));

const TeamsTable = ({ teams, authUser }) => {
  const classes = useStyles();
  return (
    <Table stickyHeader aria-label="sticky table">
      <TableHead>
        <TableRow>
          <TableCell
            style={{ minWidth: 100 }}
            className={classes.tableHead}
            colSpan="2"
          >
            <Typography variant="h6" component="h2">
              Team memberships
            </Typography>
          </TableCell>
        </TableRow>
      </TableHead>
      {
        <TableBody>
          {teams ? (
            Object.values(teams).map((team) => (
              <TableRow key={Object.values(teams).indexOf(team)}>
                <TableCell>{team.name}</TableCell>
                <TableCell>
                  {(authUser.isSuperuser ||
                    authUser.teamMemberships[team]) && (
                    <Link
                      to={routes.groupCardSummary.route.path.replace(
                        ":teamId",
                        team.id
                      )}
                    >
                      <Button
                        variant="outlined"
                        color="default"
                        size="small"
                        startIcon={<LaunchIcon />}
                      >
                        View
                      </Button>
                    </Link>
                  )}
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell>Nothing to display</TableCell>
            </TableRow>
          )}
        </TableBody>
      }
    </Table>
  );
};

TeamsTable.propTypes = {
  teams: PropTypes.object,
};

export default TeamsTable;
