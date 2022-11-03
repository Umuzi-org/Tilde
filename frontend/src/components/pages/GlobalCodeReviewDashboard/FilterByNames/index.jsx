import React from "react";
import Presentation from "./Presentation";

export default function FilterByNames({
  allNames,
  filterInclude,
  filterExclude,
  onChange,
  searchTerm,
  handleChangeSearchTerm,
  filterGroupName,
}) {
  allNames = allNames || [];
  filterInclude = filterInclude || [];
  filterExclude = filterExclude || [];
  const allFilters = [...filterInclude, ...filterExclude];

  const props = {
    allNames,
    filterExclude,
    onChange,
    searchTerm,
    handleChangeSearchTerm,
    filterGroupName,
    allFilters,
  };
  return <Presentation {...props} />;
}
