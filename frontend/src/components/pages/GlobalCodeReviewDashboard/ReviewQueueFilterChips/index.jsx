import React from "react";
import Presentation from "./Presentation";

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
          let newSelectedFilter;
          // toggle sort order only when a filter is already selected
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
  const props = {
    orderFilters,
    setFiltersMethod,
    setSelectedFilterMethod,
    handleClick,
  };
  return <Presentation {...props} />;
}
