import React from "react";
import { Link } from "react-router-dom";
import Tab from "@material/react-tab";

import {
    Button,
  } from "@material-ui/core";

export default ({to, label,selected}) => {

    const variant = selected ? "contained" : "outlined"
    return (

        <Link
        to={to}
      >
        <Button size="small" variant={variant}>
          {label}
        </Button>
        {/* <Tab size="medium" variant={variant}>{label}</Tab> */}
      </Link>
    )
}