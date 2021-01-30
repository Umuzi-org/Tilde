import React from "react";

import { Typography, Paper, Grid } from "@material-ui/core";
import ReviewCard from "../../widgets/ReviewCard";

export default ({
  reviewsDone,
  reviewsRecieved,
  handleClickOpenProjectDetails,
}) => {
  return (
    <Grid container>
      <Grid>
        <Paper>
          <Typography variant="h4">Competence Reviews Done</Typography>
          {reviewsDone.map((review) => (
            <ReviewCard
              review={review}
              key={review.id}
              handleClickOpenProjectDetails={() =>
                handleClickOpenProjectDetails({ review })
              }
              showReviewer={false}
              showReviewed={true}
            />
          ))}
        </Paper>
      </Grid>
      <Grid>
        <Paper>
          <Typography variant="h4">Competence Reviews Recieved</Typography>

          {reviewsRecieved.map((review) => (
            <ReviewCard
              review={review}
              key={review.id}
              handleClickOpenProjectDetails={() =>
                handleClickOpenProjectDetails({ review })
              }
              showReviewer={true}
              showReviewed={false}
            />
          ))}
        </Paper>
      </Grid>
    </Grid>
  );
};
