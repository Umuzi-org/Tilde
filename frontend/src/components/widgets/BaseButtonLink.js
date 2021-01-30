import React from "react";
import { Link } from "react-router-dom";

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
      </Link>
    )
}