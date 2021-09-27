import React from "react";
import { makeStyles } from "@material-ui/core/styles";

export default ({ email }) => {

  return <div>
      <form>
            <p>Email: {email}</p>

          <input type="password"></input>
          <input type="password"></input>
            <button>Submit</button>
      </form>
  </div>;
};