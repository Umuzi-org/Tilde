import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

import SummaryCard from "./SummaryCard";

import ViewContentButtonSmall from "../../../widgets/ViewContentButton";

const useStyles = makeStyles((theme) => {
  return {
    cell: {
      width: theme.spacing(30),
    },
  };
});

export default ({ columns, rows }) => {
  const classes = useStyles();
  return (
    <Paper>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell></TableCell>
            {columns.map((column) => {
              return (
                <TableCell key={column.id} className={classes.cell}>
                  {/* <Typography variant="caption">
                  [order:{column.order}]
                </Typography> */}
                  <Typography variant="subtitle1">{column.label}</Typography>
                  <ViewContentButtonSmall
                    contentUrl={column.url}
                    contentItemId={column.id}
                  />
                </TableCell>
              );
            })}
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.keys(rows)
            .sort()
            .map((name, index) => {
              const row = rows[name];
              return (
                <TableRow key={index}>
                  <TableCell>{name}</TableCell>
                  {columns.map((column) => {
                    return (
                      <TableCell key={column.id} className={classes.cell}>
                        <SummaryCard card={row[column.id]} />
                        {/* {row[column.id].status} */}
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </Paper>
  );
};
