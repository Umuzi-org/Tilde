import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

import ExpansionPanel from "@material-ui/core/ExpansionPanel";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails";
import Typography from "@material-ui/core/Typography";

import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import { TableRow, TableHead } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import CircularProgress from "@material-ui/core/CircularProgress";

import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles((theme) => ({
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },

  container: {
    maxHeight: 440,
  },

  selectedRow: {
    backgroundColor: theme.palette.primary.light,
  },

  unselectedRow: {
    cursor: "pointer",
  },
}));

export default function Presentation({
  cohorts,
  handleSelectCohortToView,
  viewCohortId,
  handleSelectRecruitToView,
  viewRecruitUserEmail,
  currentCohort,
  filterByRecruitValue,
  filterByCohortValue,
  handleChangeFilterByCohort,
  handleChangeFilterByRecruit,
  loading,
}) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <ExpansionPanel>
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography className={classes.heading}>
            App Filter options:
            {currentCohort && (
              <React.Fragment>
                Selected Cohort: C{currentCohort.label}{" "}
              </React.Fragment>
            )}
            {viewRecruitUserEmail && (
              <React.Fragment>
                Selected User: {viewRecruitUserEmail}{" "}
              </React.Fragment>
            )}
          </Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          {loading ? (
            <div>
              <CircularProgress />
            </div>
          ) : (
            <Grid container>
              <Grid item xs={4} className={classes.grid}>
                <TableContainer className={classes.container}>
                  <Table stickyHeader>
                    <TableHead>
                      <TableRow>
                        <TableCell>
                          <TextField
                            label="Select Cohort"
                            onChange={handleChangeFilterByCohort}
                            value={filterByCohortValue}
                            variant="outlined"
                          />
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {cohorts.map((cohort) => {
                        const cohortId = cohort.id;
                        const className =
                          viewCohortId === cohortId
                            ? classes.selectedRow
                            : classes.unselectedRow;

                        return (
                          <TableRow
                            className={className}
                            key={cohortId}
                            hover={viewCohortId !== cohortId}
                          >
                            <TableCell
                              onClick={() => handleSelectCohortToView(cohortId)}
                            >
                              C{cohort.label}
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
              {viewCohortId ? (
                <Grid item xs={4} className={classes.grid}>
                  <TableContainer className={classes.container}>
                    <Table stickyHeader>
                      <TableHead>
                        <TableRow>
                          <TableCell>
                            <TextField
                              label={`C${currentCohort.label} recruits`}
                              onChange={handleChangeFilterByRecruit}
                              value={filterByRecruitValue}
                              variant="outlined"
                            />
                          </TableCell>
                        </TableRow>
                      </TableHead>

                      <TableBody>
                        {currentCohort.filteredCohortRecruitUserEmails.map(
                          (userEmail) => {
                            const className =
                              viewRecruitUserEmail === userEmail
                                ? classes.selectedRow
                                : classes.unselectedRow;
                            return (
                              <TableRow
                                className={className}
                                key={userEmail}
                                onClick={() =>
                                  handleSelectRecruitToView(userEmail)
                                }
                                hover={viewRecruitUserEmail !== userEmail}
                              >
                                <TableCell>{userEmail}</TableCell>
                              </TableRow>
                            );
                          }
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Grid>
              ) : (
                <React.Fragment />
              )}
            </Grid>
          )}
        </ExpansionPanelDetails>
      </ExpansionPanel>
    </div>
  );
}
