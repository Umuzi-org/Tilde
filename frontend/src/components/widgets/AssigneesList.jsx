import React from "react";
// import { Typography } from "@material-ui/core";
import { Table, TableBody, TableRow, TableCell } from "@material-ui/core";

export default ({ userNames, userIds }) => {
  return (
    <Table size="small">
      <TableBody>
        {userNames.map((name) => (
          <TableRow>
            <TableCell padding="none">{name}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
  // return <Typography>{userNames.join(", ")}</Typography>;
};
