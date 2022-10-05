import React from "react";
import Modal from "../../widgets/Modal";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import CloseIcon from "@material-ui/icons/Close";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import TextareaAutosize from "@material-ui/core/TextareaAutosize";
import Alert from "@material-ui/lab/Alert";
import Button from "../../widgets/Button";
import CardButton from "../../widgets/CardButton";
import { makeStyles } from "@material-ui/core/styles";
import StatusHelp from "./StatusHelp";

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: 120,
  },
  alert: {
    marginBottom: theme.spacing(1),
  },
  paper: {
    padding: theme.spacing(1),
  },
  textArea: {
    width: "100%",
  },
  rightButton: {
    float: "right",
  },
  exitIcon: {
    marginBottom: "0.5rem",
  },
}));

export default function Presentation({
  card,
  handleSubmit,
  status,
  comments,
  formErrors,
  closeModal,
  statusChoices,
  loading,
}) {
  const classes = useStyles();

  if (!card) {
    return <React.Fragment />;
  }

  return (
    <Modal open={!!card} onClose={closeModal}>
      <Paper className={classes.paper}>
        <Grid container>
          <Grid item xs={10} sm={11}>
            <Typography variant="h5">
              Add Review for {card.contentType}: {card.title}
            </Typography>
          </Grid>
          <Grid item xs={2} sm={1} className={classes.exitIcon}>
            <Button variant="outlined" onClick={closeModal}>
              <CloseIcon />
            </Button>
          </Grid>
        </Grid>

        <Alert severity="info" className={classes.alert}>
          Whatever you write here will be visible to staff and to the person you
          are reviewing. Take the time to give an accurate and useful review
        </Alert>

        <form noValidate onSubmit={handleSubmit}>
          {formErrors}

          <Grid container spacing={1}>
            <Grid item xs={12}>
              <FormControl
                variant="outlined"
                className={classes.formControl}
                fullWidth
              >
                <InputLabel id="demo-simple-select-outlined-label" required>
                  Status
                </InputLabel>
                <Select
                  labelId="demo-simple-select-outlined-label"
                  id="demo-simple-select-outlined"
                  label="Status"
                  {...status}
                >
                  {Object.keys(statusChoices).map((key) => {
                    return (
                      <MenuItem key={key} value={key}>
                        {statusChoices[key]}
                      </MenuItem>
                    );
                  })}
                </Select>
              </FormControl>
              <StatusHelp />
            </Grid>
            <Grid item xs={12}>
              <TextareaAutosize
                className={classes.textArea}
                aria-label="your comments"
                minRows={5}
                placeholder="Your comments*"
                {...comments}
              />
            </Grid>
            <Grid item xs={6}>
              <Button variant="outlined" onClick={closeModal}>
                Cancel
              </Button>
            </Grid>
            <Grid item xs={6}>
              <CardButton
                type="submit"
                variant="outlined"
                className={classes.rightButton}
                loading={loading}
                label="Submit your review"
                onClick={handleSubmit}
              ></CardButton>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Modal>
  );
}
