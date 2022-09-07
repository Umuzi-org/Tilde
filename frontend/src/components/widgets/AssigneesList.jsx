import React from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import UserAvatarLink from "../widgets/UserAvatarLink";

export default function AssigneesList({ userNames, userIds }) {
  return (
    <Table size="small">
      <TableBody>
        {userNames.map((name) => (
          <TableRow key={userIds}>
            <TableCell padding="none">
              <UserAvatarLink email={name} userId={userIds} />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
