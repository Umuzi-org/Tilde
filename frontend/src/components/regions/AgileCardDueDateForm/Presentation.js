import React from 'react';
import { makeStyles } from '@mui/material/styles';

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

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