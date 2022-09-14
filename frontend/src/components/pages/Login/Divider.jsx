import React from "react";
import { Grid, Divider as MuiDivider } from "@material-ui/core";

export default function Divider({ children, ...props }) {
  return (
    <Grid container alignItems="center" spacing={3} {...props}>
      <Grid item xs>
        <MuiDivider />
      </Grid>
      <Grid item>{children}</Grid>
      <Grid item xs>
        <MuiDivider />
      </Grid>
    </Grid>
  );
}
