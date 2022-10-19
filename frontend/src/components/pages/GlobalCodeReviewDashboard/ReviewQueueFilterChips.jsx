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

export default function ReviewQueueFilterChips({
  orderFilters,
  setFiltersMethod,
  setSelectedFilterMethod,
}) {
  const classes = useStyles();

  function handleClick({
    setFiltersMethod,
    setSelectedFilterMethod,
    selectedFilter,
  }) {
    setFiltersMethod((prev) => {
      return prev.map((filter) => {
        if (filter.label === selectedFilter.label) {
          let newSelectedFilter;
          // toggle filter sort order only when a filter is already selected
          if (filter.isSelected) {
            newSelectedFilter = {
              ...filter,
              isSelected: true,
              isAscending: !filter.isAscending,
            };
          } else {
            newSelectedFilter = { ...filter, isSelected: true };
          }
          setSelectedFilterMethod(newSelectedFilter);
          return newSelectedFilter;
        } else {
          return { ...filter, isSelected: false };
        }
      });
    });
  }

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
