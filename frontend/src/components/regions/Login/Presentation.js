// import React from "react";
// import { makeStyles } from "@material-ui/core/styles";
// import Button from "@material-ui/core/Button";
// import Typography from "@material-ui/core/Typography";

// import { Paper } from "@material-ui/core";
// import Alert from "@material-ui/lab/Alert";

// const useStyles = makeStyles((theme) => ({
//   root: {
//     margin: theme.spacing(2),
//     // padding: theme.spacing(2),
//   },
//   button: {
//     margin: theme.spacing(1),
//   },
//   alert: {
//     margin: theme.spacing(1),
//   },
// }));

// export default ({ loading, error, handleLoginWithGoogle }) => {
//   const classes = useStyles();

//   return (
//     <Paper className={classes.root}>
//       <Typography variant="h6">Please log in</Typography>

//       <Alert severity="info" className={classes.alert}>
//         Note that this site uses popups for authentication
//       </Alert>

//       {error && (
//         <Alert severity="error" className={classes.alert}>
//           ERROR: {error}. You might need to refresh this page to attempt to
//           login again
//         </Alert>
//       )}

//       <Button
//         className={classes.button}
//         variant="contained"
//         onClick={handleLoginWithGoogle}
//       >
//         Login with Google
//       </Button>
//     </Paper>
//   );
// };

import React from "react"
import {Grid, Paper, TextField, Button} from "@material-ui/core"
import {createTheme, responsiveFontSizes, ThemeProvider} from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"

let theme = createTheme()
theme = responsiveFontSizes(theme)

const Login = () => {

  const paperStyle = {
    padding: 20,
    height: "relative",
    width: "relative",
    margin: "30% auto",
  }

  const buttonStyle = {
    marginTop: 20,
  }

  return (
      <Grid>
        <Paper elevation={10} style={paperStyle}>
          <Grid align="center">
          <ThemeProvider theme={theme}> 
            <Typography variant="h3">Login</Typography>
          </ThemeProvider>
          </Grid>
          <div align="center">
            <TextField label="Email" type="email" required/><br/>
            <TextField label="Password" type="password" required/>
          </div>
          <div align="center">
            <Button type="submit" variant="contained" color="primary" style={buttonStyle}>Login</Button>
          </div>
        </Paper>
      </Grid>
    )
}

export default Login