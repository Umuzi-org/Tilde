import React from "react";

import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

export default ({ loading, error, handleLoginWithGoogle }) => {
  return (
    <React.Fragment>
      <Typography>
        Please log in. Use your @umuzi.org email address if you have one
      </Typography>

      <Typography>
        Note that this site uses popups for authentication.
      </Typography>

      {error && (
        <Typography>
          ERROR: {error}. You might need to refresh this page to attempt to
          login again
        </Typography>
      )}

      <Button onClick={handleLoginWithGoogle}>Login with Google</Button>
    </React.Fragment>
  );
};

// TODO: make this look better needsissue
