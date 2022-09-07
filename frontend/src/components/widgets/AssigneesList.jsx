import React from "react";
// import { Typography } from "@material-ui/core";
import { Table, TableBody, TableRow, TableCell } from "@material-ui/core";
import UserAvatarLink from "../widgets/UserAvatarLink";

export default ({ userNames, userIds }) => {
  return (
    <Table size="small">
      <TableBody>
        {userNames.map((name) => (
          <TableRow>
            <TableCell padding="none">
              <UserAvatarLink email={name} userId={userIds} />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
  // return <Typography>{userNames.join(", ")}</Typography>;
};
