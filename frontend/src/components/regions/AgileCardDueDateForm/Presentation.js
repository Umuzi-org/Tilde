import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles({

    dueDateButton: {
        height: "1.5rem",
        marginTop: "0.3rem",
        marginRight: "0.3rem",
    },
});

const AgileCardDueDateForm = (props) => {

    const { dueDateInstance } = props;
    const classes = useStyles();

    return (
        <Grid container sm={12}>
          <Grid item container>
            <form className={classes.container} noValidate>
              <TextField item
                id="date"
                label="Due Date:"
                type="date"
                defaultValue=""
                className={classes.textField}
                InputLabelProps={{
                  shrink: true,
                }}
              />
              <Grid item container>
                <Button className={classes.dueDateButton} variant="outlined">Save</Button>
                <Button className={classes.dueDateButton} variant="outlined">Cancel</Button>
              </Grid>
            </form>
          </Grid>
        </Grid>
    )
}

export default AgileCardDueDateForm;
