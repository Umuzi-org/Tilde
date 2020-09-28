import React from "react";
// import Modal from "../../widgets/Modal";
// import { Typography, Paper, Button, Grid } from "@material-ui/core";

// import DateFnsUtils from "@date-io/date-fns";
// import {
//   MuiPickersUtilsProvider,
//   KeyboardTimePicker,
//   KeyboardDatePicker,
// } from "@material-ui/pickers";
// import { makeStyles } from "@material-ui/core/styles";

// const useStyles = makeStyles((theme) => ({
//   paper: {
//     padding: theme.spacing(1),
//   },
//   rightButton: {
//     float: "right",
//   },
// }));

export default ({ card, handleSubmit, closeModal, date, time, formErrors }) => {
  //   const card = {
  //     id: 1,
  //     contentItem: 1,
  //     contentItemUrl:
  //       "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/projects/tdd/simple-calculator/part-1/_index.md",
  //     status: "R",
  //     recruitProject: 1,
  //     assignees: [2],
  //     reviewers: [],
  //     assigneeNames: ["sheena.oconnell@gmail.com"],
  //     reviewerNames: [],
  //     isHardMilestone: true,
  //     isSoftMilestone: true,
  //     title: "something awesome part 1",
  //     contentType: "workshop",
  //     storyPoints: 5,
  //     tags: ["tag1"],
  //     order: 1,
  //   };
  if (!card) {
    return <React.Fragment />;
  }
  //   const classes = useStyles();

  throw new Error("Not implemented");
  //   const selectedDate = new Date("2014-08-18T21:11:54");
  //   return (
  //     <Modal open={!!card} onClose={closeModal}>
  //       <Paper className={classes.paper}>
  //         <Typography variant="h5">
  //           Add Attendance for workshop: {card.title}
  //         </Typography>
  //         <MuiPickersUtilsProvider utils={DateFnsUtils}>
  //           <form noValidate onSubmit={handleSubmit}>
  //             {formErrors}
  //             <Grid container justify="space-around">
  //               <Grid item xs={6}>
  //                 {/* <KeyboardDatePicker
  //                   disableToolbar
  //                   variant="inline"
  //                   format="MM/dd/yyyy"
  //                   margin="normal"
  //                   id="date-picker-inline"
  //                   label="Date picker inline"
  //                   {...date}
  //                   value={selectedDate}
  //                   KeyboardButtonProps={{
  //                     "aria-label": "change date",
  //                   }}
  //                 /> */}
  //               </Grid>
  //               <Grid item xs={6}>
  //                 {/* <KeyboardTimePicker
  //                   margin="normal"
  //                   id="time-picker"
  //                   label="Time picker"
  //                   //   value={selectedDate}
  //                   //   onChange={handleDateChange}
  //                   {...time}
  //                   KeyboardButtonProps={{
  //                     "aria-label": "change time",
  //                   }}
  //                 /> */}
  //               </Grid>
  //               <Grid item xs={6}>
  //                 <Button variant="outlined" onClick={closeModal}>
  //                   Cancel
  //                 </Button>
  //               </Grid>
  //               <Grid item xs={6}>
  //                 <Button
  //                   type="submit"
  //                   variant="outlined"
  //                   className={classes.rightButton}
  //                 >
  //                   Save
  //                 </Button>
  //               </Grid>
  //             </Grid>
  //           </form>
  //         </MuiPickersUtilsProvider>
  //       </Paper>
  //     </Modal>
  //   );
};
