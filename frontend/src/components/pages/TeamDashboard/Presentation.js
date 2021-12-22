import React from "react";
import {
  Grid,
  Paper,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
}));

export default ({ team }) => {
  const classes = useStyles();
  if (team)
    return (
      <React.Fragment>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <Table>
                <TableBody>
                  {team.members.map((member) => (
                    <TableRow key={member.userId}>
                      <TableCell>
                        <Typography>{member.userEmail}</Typography>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>
          </Grid>
        </Grid>
      </React.Fragment>
    );
  return <React.Fragment />; // TODO: loading. update story to show this
};
