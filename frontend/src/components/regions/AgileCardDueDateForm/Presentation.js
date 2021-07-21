import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles({

    dueDateButton: {
        height: "1.6rem",
        marginTop: "0.3rem",
        marginRight: "0.3rem",
    },
});

const AgileCardDueDateForm = (props) => {

  const { dueTime } = props;
  const defaultValue = dueTime ? dueTime.split('').slice(0, 16).join('') : "";
  const classes = useStyles();

  return (
    <Grid container sm={12} justifyContent="center">
      <form className={classes.container} noValidate>
        <TextField item
          id="datetime-local"
          label="Due Date:"
          type="datetime-local"
          defaultValue={defaultValue}
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
        />
        <Grid item container sm={12}>
          <Button className={classes.dueDateButton} variant="outlined">Save</Button>
          <Button className={classes.dueDateButton} variant="outlined">Cancel</Button>
        </Grid>
      </form> 
    </Grid>
  )
}

export default AgileCardDueDateForm;