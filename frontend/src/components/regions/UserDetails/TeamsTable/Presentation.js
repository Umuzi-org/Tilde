import React from "react";
import PropTypes from "prop-types";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { makeStyles } from "@mui/material/styles";
import { Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { routes } from "../../../../routes";
import LaunchIcon from "@mui/icons-material/Launch";

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
                    authUser.permissions.teams[team.id]) && (
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
