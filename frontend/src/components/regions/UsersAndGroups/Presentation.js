import React from "react";
import { makeStyles } from "@material-ui/core/styles";

import {
  TableRow,
  TableHead,
  TextField,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
} from "@material-ui/core";

// import FilterListIcon from "@material-ui/icons/FilterList";

const useStyles = makeStyles((theme) => ({}));

export default function Presentation({
  userGroups,
  users,
  filterByGroup,
  filterByUser,
}) {
  const classes = useStyles();
  return (
    <Grid container>
      <Grid item xs={4} className={classes.grid}>
        <TableContainer className={classes.container}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>
                  <TextField
                    label="User Groups"
                    variant="outlined"
                    {...filterByGroup}
                  />
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {userGroups.map((group) => {
                return (
                  <TableRow key={group.id}>
                    <TableCell>{group.name}</TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>

      <Grid item xs={4} className={classes.grid}>
        <TableContainer className={classes.container}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>
                  <TextField
                    label="Users"
                    variant="outlined"
                    {...filterByUser}
                  />
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.keys(users).map((email) => {
                return (
                  <TableRow key={email}>
                    <TableCell>{email}</TableCell>
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
