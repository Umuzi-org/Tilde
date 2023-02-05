import React from "react";
import Modal from "../../widgets/Modal";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import CloseIcon from "@material-ui/icons/Close";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import TextField from "@material-ui/core/TextField";
import Alert from "@material-ui/lab/Alert";
import Button from "../../widgets/Button";
import CardButton from "../../widgets/CardButton";
import { makeStyles } from "@material-ui/core/styles";
import StatusHelp from "./StatusHelp";
import IconButton from "@material-ui/core/IconButton";
import FormHelperText from "@material-ui/core/FormHelperText";

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: 120,
  },
  alert: {
    marginBottom: theme.spacing(1),
  },

  textArea: {
    width: "100%",
  },

  buttons: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: theme.spacing(1),
  },
  statusHelp: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
}));

export default function Presentation({
  card,
  handleSubmit,
  handleOnChange,
  formValues,
  formFieldHasError,
  formFieldError,
  closeModal,
  statusChoices,
  loading,
}) {
  const classes = useStyles();

  if (!card) {
    return <React.Fragment />;
  }

  const title = `Add Review for ${card.contentType}: ${card.title}`;

  return (
    <Modal open={!!card} onClose={closeModal} title={title}>
      {(formFieldHasError("status") || formFieldHasError("comments")) && (
        <Alert severity="error" className={classes.alert}>
          An error occurred while trying to submit your review
        </Alert>
      )}

      <Alert severity="info" className={classes.alert}>
        Whatever you write here will be visible to staff and to the person you
        are reviewing. Take the time to give an accurate and useful review
      </Alert>

      <form noValidate onSubmit={handleSubmit}>
        <Grid container>
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
                name="status"
                value={formValues.status}
                onChange={handleOnChange}
                error={formFieldHasError("status")}
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
            {formFieldHasError("status") && (
              <FormHelperText error={true}>
                {formFieldError("status")}
              </FormHelperText>
            )}
            <Grid className={classes.statusHelp}>
              <StatusHelp />
            </Grid>
          </Grid>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              aria-label="your comments"
              id="outlined-multiline-static"
              label="Your comments"
              multiline
              rows={15}
              placeholder="Nicely done :)"
              fullWidth
              name="comments"
              value={formValues.comments}
              onChange={handleOnChange}
              error={formFieldHasError("comments")}
              required
            />
            {formFieldHasError("comments") && (
              <FormHelperText error={true}>
                {formFieldError("comments")}
              </FormHelperText>
            )}
          </Grid>
          <Grid container className={classes.buttons}>
            <Grid item>
              <Button variant="outlined" onClick={closeModal}>
                Cancel
              </Button>
            </Grid>
            <Grid item>
              <CardButton
                type="submit"
                variant="outlined"
                loading={loading}
                label="Submit your review"
                onClick={handleSubmit}
              ></CardButton>
            </Grid>
          </Grid>
        </Grid>
      </form>
    </Modal>
  );
}
