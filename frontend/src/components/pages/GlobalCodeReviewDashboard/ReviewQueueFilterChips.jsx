import React from "react";
import Chip from "@material-ui/core/Chip";
import Typography from "@material-ui/core/Typography";

export default function ReviewQueueFilterChips({
  orderFilters,
  setFiltersMethod,
  setSelectedFilterMethod,
}) {
  function handleClick({
    setFiltersMethod,
    setSelectedFilterMethod,
    selectedFilter,
  }) {
    setFiltersMethod((prev) => {
      return prev.map((filter) => {
        if (filter.label === selectedFilter.label) {
          const newSelectedFilter = { ...filter, isSelected: true };
          setSelectedFilterMethod(newSelectedFilter);
          return { ...filter, isSelected: true };
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
        orderFilters.map((filter) => (
          <Chip
            label={filter.label}
            variant={filter.isSelected ? "default" : "outlined"}
            onClick={() =>
              handleClick({
                setFiltersMethod: setFiltersMethod,
                setSelectedFilterMethod: setSelectedFilterMethod,
                selectedFilter: filter,
              })
            }
          />
        ))}
    </>
  );
}
