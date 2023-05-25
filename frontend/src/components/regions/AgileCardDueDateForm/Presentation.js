import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles({

    dueTimeButton: {
        marginTop: "0.3rem",
        marginRight: "0.3rem",
    },
});

const AgileCardDueDateForm = (props) => {

  const { dueTime } = props;
  const defaultValue = dueTime ? dueTime.split('').slice(0, 16).join('') : "";
  const classes = useStyles();

  return (
      <form novalidate>
        <TextField
          id="datetime-local"
          label="Due Date:"
          type="datetime-local"
          defaultValue={defaultValue}
          InputLabelProps={{
            shrink: true,
          }}
        />
        <Grid container>
          <Button className={classes.dueTimeButton} variant="outlined">Save</Button>
          <Button className={classes.dueTimeButton} variant="outlined">Cancel</Button>
        </Grid>
      </form> 
  )
}

export default AgileCardDueDateForm;