// import React from "react";
// import {
//   Paper,
//   Table,
//   TableContainer,
//   TableHead,
//   TableBody,
//   TableRow,
//   TableCell,
//   Typography,
// } from "@material-ui/core";
// import { makeStyles } from "@material-ui/core/styles";
// import Markdown from "react-markdown";

// import ReviewStatus from "../../widgets/ReviewStatus";
// import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";

// const useStyles = makeStyles((theme) => ({
//   paper: {
//     padding: theme.spacing(1, 2, 1),
//   },

//   commentColumn: {
//     minWidth: 300,
//     maxWidth: 300,
//   },

//   tableContainer: {
//     maxHeight: 200,
//   },

//   sectionPaper: {
//     padding: theme.spacing(1),
//     marginBottom: theme.spacing(1),
//     maxWidth: "100%",
//     maxHeight: "100%",
//   },
// }));

// export default ({ reviewIds, reviews }) => {
//   const classes = useStyles();
//   let body;
//   if (reviewIds.length) {
//     if (reviews.length) {
//       body = (
//         <React.Fragment>
//           {reviews.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).map((review) => {
//             const timestamp = new Date(review.timestamp);
//             return (
//               <TableRow key={review.id}>
//                 <TableCell>{timestamp.toLocaleString()}</TableCell>
//                 <TableCell>
//                   <ReviewStatus status={review.status} />
//                 </TableCell>
//                 <TableCell>{review.reviewerUserEmail}</TableCell>
//                 <TableCell className={classes.commentColumn}>
//                   <Markdown source={review.comments}></Markdown>
//                 </TableCell>
//                 <TableCell>
//                   <ReviewValidationIcons review={review} />
//                 </TableCell>
//               </TableRow>
//             );
//           })}
//         </React.Fragment>
//       );
//     } else {
//       body = (
//         <TableRow>
//           <TableCell colSpan="4">Loading...</TableCell>
//         </TableRow>
//       );
//     }
//   } else {
//     body = (
//       <TableRow>
//         <TableCell colSpan="4">No reviews yet</TableCell>
//       </TableRow>
//     );
//   }

//   return (
//     <Paper className={classes.sectionPaper} variant="outlined">
//       <Typography variant="h6">Reviews</Typography>
//       <TableContainer className={classes.tableContainer}>
//         <Table stickyHeader aria-label="sticky table">
//           <TableHead>
//             <TableRow>
//               <TableCell>timestamp</TableCell>
//               <TableCell>Status</TableCell>
//               <TableCell>reviewer</TableCell>
//               <TableCell>Comments</TableCell>
//               <TableCell></TableCell>
//             </TableRow>
//           </TableHead>
//           <TableBody>{body}</TableBody>
//         </Table>
//       </TableContainer>
//     </Paper>
//   );
// };
import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import CardActions from "@material-ui/core/CardActions";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import Chip from "@material-ui/core/Chip";
import {
  createTheme,
  responsiveFontSizes,
  MuiThemeProvider,
} from "@material-ui/core";

import ReviewStatus from "../../widgets/ReviewStatus";
import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: false,
    transition: "transform 0.15s ease-in-out",
    "&:hover": { transform: "scale3d(1.05, 1.05, 1)" }
  },
}));

export default function Reviews() {
  const classes = useStyles();

  let theme = createTheme();
  theme = responsiveFontSizes(theme);

  const review =
    "This is good work an this text is really long and that os that makes a ndf jn fja ajf afn afjdn afdn anf nadfadfnia njadnfadf b asdidf jf daasdfn jkn sdfb shvb  vnxvs done on purpose to test that this component can handle a lot of text inside it";
  const email = "sheena.oconnell@umuzi.org";

  return (
    <Card className={classes.root}>
      <MuiThemeProvider theme={theme}>
        <CardHeader
          title={
            <Typography gutterBottom variant="h5" component="h5">
              {email}
            </Typography>
          }
          subheader={Date.now()}
        />
        <CardContent>
          <Typography variant="body1" component="p">
            {review}
          </Typography>
        </CardContent>
        <CardActions disableSpacing>
          <IconButton>
            <Chip variant="outlined" size="medium" label="competent" />
          </IconButton>
          <IconButton>
            <CheckCircleIcon />
          </IconButton>
        </CardActions>
      </MuiThemeProvider>
    </Card>
  );
}
