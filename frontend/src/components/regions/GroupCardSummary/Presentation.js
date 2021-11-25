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
import LinkToUserBoard from "../../widgets/LinkToUserBoard";
import Loading from "../../widgets/Loading";

const useStyles = makeStyles((theme) => {
  return {
    cell: {
      width: theme.spacing(30),
    },
    sticky: {
      // position: "-webkit-sticky",
      position: "sticky",
      background: "#fff",
      left: 0,
      zIndex: 1,

     ['@media (max-width:780px)']: { // eslint-disable-line no-useless-computed-key
        background: "none",
      }, 
    },
    title: {
      marginLeft: "16px",
      ['@media (max-width:780px)']: { // eslint-disable-line no-useless-computed-key
        fontSize: "1.5rem",
        marginLeft: "16px",
      }, 
    },

    container: {
      // width: 912 - 200,
      // height: 976 - 300,
      // height: `calc(100% - {theme.spacing(20)px})`,
      overflow: "auto",
    },
  };
});

export default ({
  userGroup,
  columns,
  rows,
  displayUsers,
  apiCallData,
  handleScroll,
}) => {
  const classes = useStyles();

  return (
    <React.Fragment>
      <Typography className={classes.title} variant="h4">{userGroup.name}</Typography>

      <div className={classes.container} onScroll={handleScroll}>
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
            {Object.keys(displayUsers)
              .sort()
              .map((userId, index) => {
                const row = rows[userId] || {};
                return (
                  <TableRow key={index}>
                    <TableCell className={classes.sticky}>
                      <Typography>{displayUsers[userId]}</Typography>
                      <LinkToUserBoard userId={userId} />
                    </TableCell>

                    {apiCallData[userId].loading &&
                      Object.keys(row).length === 0 && (
                        <TableCell>
                          <Loading />
                        </TableCell>
                      )}

                    {columns.map((column) => {
                      return (
                        <TableCell key={column.id} className={classes.cell}>
                          <CellContent card={row[column.id]} />
                        </TableCell>
                      );
                    })}

                    {apiCallData[userId].loading &&
                      Object.keys(row).length > 0 && (
                        <TableCell>
                          <Loading />
                        </TableCell>
                      )}
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </div>
    </React.Fragment>
  );
};
