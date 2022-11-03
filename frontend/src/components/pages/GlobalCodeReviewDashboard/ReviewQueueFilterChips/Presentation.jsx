import React from "react";
import Chip from "@material-ui/core/Chip";
import Typography from "@material-ui/core/Typography";
import ArrowDownwardIcon from "@material-ui/icons/ArrowDownward";
import ArrowUpwardIcon from "@material-ui/icons/ArrowUpward";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => {
  return {
    chip: {
      margin: theme.spacing(0.5),
    },
  };
});

export default function Presentation({
  orderFilters,
  setFiltersMethod,
  setSelectedFilterMethod,
  handleClick,
}) {
  const classes = useStyles();

  return (
    <>
      <Typography>Sort by:</Typography>
      {orderFilters &&
        orderFilters.map((filter, index) => {
          const sortOrderIcon = filter.isAscending ? (
            <ArrowUpwardIcon />
          ) : (
            <ArrowDownwardIcon />
          );
          return (
            <Chip
              key={`${filter}_${index}`}
              label={filter.label}
              icon={sortOrderIcon}
              variant={filter.isSelected ? "default" : "outlined"}
              onClick={() =>
                handleClick({
                  setFiltersMethod: setFiltersMethod,
                  setSelectedFilterMethod: setSelectedFilterMethod,
                  selectedFilter: filter,
                })
              }
              className={classes.chip}
            />
          );
        })}
    </>
  );
}
