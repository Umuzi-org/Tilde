// import React from "react";
// import Badge from "@material-ui/core/Badge";
// import { makeStyles, withStyles } from "@material-ui/core/styles";
// import Avatar from "@material-ui/core/Avatar";
// import EditTwoToneIcon from "@material-ui/core/EditTwoToneIcon"

// // export default function ProfilePicture() {
// // return (
// //   <Avatar
// //     src="https://cdnb.artstation.com/p/assets/images/images/033/885/779/large/caio-fernandes-1288b8b9-187d-4812-a73f-1dd14c9bb8d3.jpg?1610822483"
// //     variant="square"
// //     style={{ width: "100%", height: "100%" }}
// //   >
// //     SD
// //   </Avatar>
// // );

// // }

// const StyledBadge = withStyles((theme) => ({
//   badge: {
//     // backgroundColor: "#44b700",
//     color: "red",
//     boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
//     "&::after": {
//       position: "absolute",
//       bottom: 0,
//       left: 0,
//       width: "100%",
//       height: "100%",
//       borderRadius: "50%",
//       animation: "$ripple 1.2s infinite ease-in-out",
//       border: "1px solid currentColor",
//       content: '""',
//     },
//   },
//   "@keyframes ripple": {
//     "0%": {
//       transform: "scale(.8)",
//       opacity: 1,
//     },
//     "100%": {
//       transform: "scale(2.4)",
//       opacity: 0,
//     },
//   },
// }))(Badge);

// // const SmallAvatar = withStyles((theme) => ({
// //   root: {
// //     width: "100%",
// //     height: "100%",
// //     border: `2px solid ${theme.palette.background.paper}`,
// //   },
// // }))(Avatar);

// const useStyles = makeStyles((theme) => ({
//   root: {
//     display: "flex",
//     "& > *": {
//       margin: theme.spacing(1),
//     },
//   },
// }));

// export default function ProfilePicture() {
//   const classes = useStyles();

//   return (
//     <div className={classes.root}>
//       <StyledBadge
//         overlap="rectangle"
//         anchorOrigin={{
//           vertical: "bottom",
//           horizontal: "right",
//         }}
//         variant="dot"
//       >
//         <Avatar
//           style={{ width: "100vw", height: "100vh" }}
//           alt="Remy Sharp"
//           src="https://cdnb.artstation.com/p/assets/images/images/033/885/779/large/caio-fernandes-1288b8b9-187d-4812-a73f-1dd14c9bb8d3.jpg?1610822483"
//         />
//       </StyledBadge>
//     </div>
//   );
// }
