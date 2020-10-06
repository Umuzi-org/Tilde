import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import {
  Table,
  Typography,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
} from "@material-ui/core";

import CellContent from "./CellContent";

const useStyles = makeStyles((theme) => {
  return {
    cell: {
      width: theme.spacing(30),
    },
  };
});

export default ({ userGroup, columns, rows }) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <Typography>{userGroup.name}</Typography>

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
                  {/* <ViewContentButtonSmall
                    contentUrl={column.url}
                    contentItemId={column.id}
                  /> */}
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
                        {/* <SummaryCard card={row[column.id]} /> */}
                        {/* {row[column.id].status} */}
                        <CellContent card={row[column.id]} />
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </React.Fragment>
  );
};
