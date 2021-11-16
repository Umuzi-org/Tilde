import React from "react";
import { Link } from "react-router-dom";

import {
    Button,
  } from "@mui/material";

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