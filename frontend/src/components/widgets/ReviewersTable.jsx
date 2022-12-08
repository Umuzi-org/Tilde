import React from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Typography from "@material-ui/core/Typography";
import Avatar from "@material-ui/core/Avatar";
import Tooltip from "@material-ui/core/Tooltip";
import Checkbox from "@material-ui/core/Checkbox";
import { makeStyles } from "@material-ui/core/styles";
import UserAvatarLink from "./UserAvatarLink";

import Loading from "../widgets/Loading";

const useStyles = makeStyles((theme) => {
  return {
    reviewer: {
      width: theme.spacing(3),
      height: theme.spacing(3),
    },
  };
});

function ReviewersTable({
  reviewerUsers,
  reviewerUserEmails,
  usersThatReviewedSinceLastReviewRequestEmails,
  usersThatReviewedSinceLastReviewRequest,
}) {
  const classes = useStyles();
  if (!usersThatReviewedSinceLastReviewRequestEmails) {
    return <Loading />;
  }

  const allEmails = [
    ...reviewerUserEmails,
    ...usersThatReviewedSinceLastReviewRequestEmails,
  ];

  const allIds = [...reviewerUsers, ...usersThatReviewedSinceLastReviewRequest];

  function compare(a, b) {
    if (a.email < b.email) {
      return -1;
    }
    if (a.email > b.email) {
      return 1;
    }
    return 0;
  }

  const allUsers = [];

  allIds.forEach((id, index) => {
    if (allUsers.map((user) => user.userId).includes(id)) return;
    allUsers.push({
      userId: id,
      email: allEmails[index],
    });
  });

  allUsers.sort(compare);
  const stringIds = allUsers.filter((user) => typeof user.userId === "string");
  const numberIds = allUsers.filter((user) => typeof user.userId !== "string");
  // console.log(stringIds);
  // console.log(numberIds);
  // const arr = [];
  const arr2 = numberIds.map((obj) => {
    // console.log(obj);
    // let res;
    stringIds.map((o) => {
      if (o.email === obj.email) {
        obj = o;
      }
      // console.log("arrrrr", o.email === obj.email ? obj : o);
      // res = o.email === obj.email ? o : obj;
    });
    return obj;
  });
  // const results = numberIds.filter(
  // ({ value: obj }) => !stringIds.some(({ value: o }) => obj === o)
  // );
  // const results = numberIds.filter(
  //   ({ value: obj }) => !stringIds.some(({ value: o }) => obj.email === o.email)
  // );
  // const results = stringIds.filter(
  //   ({ value: id1 }) =>
  //     !numberIds.some(({ value: id2 }) => {
  //       // console.log(value: ids);
  //       return id2 === id1;
  //     })
  // );
  const resultFilter = (firstArray, secondArray) => {
    return firstArray.filter(
      (firstArrayItem) =>
        !secondArray.some(
          (secondArrayItem) => firstArrayItem.email === secondArrayItem.email
        )
    );
  };
  // console.log(resultFilter(stringIds, numberIds));
  Array.prototype.push.apply(arr2, resultFilter(stringIds, numberIds));
  // console.log("arr2888", arr2);
  // let arr4 = arr2;
  // const arr3 = arr2.map((obj) => {
  //   allUsers.map((o) => {
  //     // arr
  //     // arr4 = [];
  //     if (o.email !== obj.email) {
  //       // console.log("arr2888", o.email, obj.email);

  //       // arr4.push(o);
  //       obj = o;
  //     }
  //   });
  //   return obj;
  // });
  // console.log("arr2888", arr2);

  // const valueArr = allUsers.map(function (item) {
  //   return item.email;
  // });n
  // const isDuplicate = valueArr.some(function (item, idx) {
  //   if (valueArr.indexOf(item) !== idx) {
  //     return { ...idx };
  //   }
  // });
  // console.log(allUsers);
  // console.log("hello", arr4);
  // console.log("all", allUsers);

  if (arr2.length === 0) return <Typography>No reviewers!</Typography>;

  return (
    <Table size="small">
      <TableBody>
        {arr2.map((user) => {
          return (
            <TableRow key={user.userId}>
              <TableCell padding="none">
                <Checkbox
                  checked={usersThatReviewedSinceLastReviewRequest.includes(
                    user.userId
                  )}
                  disabled
                />
              </TableCell>
              <TableCell padding="none">
                {reviewerUsers.includes(user.userId) && (
                  <Tooltip title="this user is an allocated reviewer on this project">
                    <Avatar className={classes.reviewer}>R</Avatar>
                  </Tooltip>
                )}
              </TableCell>
              <TableCell>
                <UserAvatarLink email={user.email} userId={user.userId} />
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
}

export default ReviewersTable;
