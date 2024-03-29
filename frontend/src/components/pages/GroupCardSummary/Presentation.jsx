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
import Button from "../../widgets/Button";

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

      // eslint-disable-next-line no-useless-computed-key
      ["@media (max-width:780px)"]: {
        background: "none",
      },
    },

    subTitle: {
      marginLeft: "8px",
      // eslint-disable-next-line no-useless-computed-key
      ["@media (max-width:780px)"]: {
        marginLeft: "8px",
      },
    },
    container: {
      overflowBottom: "auto",
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
  fetchNextPages,
}) => {
  const classes = useStyles();

  return (
    <React.Fragment>
      <div className={classes.container} onScroll={handleScroll}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              {columns.map((column) => {
                return (
                  <TableCell key={column.id} className={classes.cell}>
                    <Typography
                      className={classes.subTitle}
                      variant="subtitle1"
                    >
                      {column.label}
                    </Typography>
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

                    {index === 0 && (
                      <TableCell rowSpan={Object.keys(rows).length}>
                        {apiCallData[userId].loading ? (
                          ""
                        ) : (
                          <Button onClick={fetchNextPages}>Load More</Button>
                        )}
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
