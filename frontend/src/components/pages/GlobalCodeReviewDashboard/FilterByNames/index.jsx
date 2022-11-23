import React, { useState } from "react";
import { filterList } from "../utils";
import Presentation from "./Presentation";

// export default function FilterByNames({
//   allNames,
//   filterInclude,
//   filterExclude,
//   onChange,
// }) {

// const [searchTerm, setSearchTerm] = useState()  // This is the only new piece of state we need

// function handleChangeSearchTerm(...){
// ...
// setSearchTerm(...)
// }

export default function FilterByNames({
  allNames,
  filterInclude,
  filterExclude,
  onChange,
  // searchTerm,
  // handleChangeSearchTerm,
  // filterGroupName,
}) {
  allNames = allNames || [];
  filterInclude = filterInclude || [];
  filterExclude = filterExclude || [];
  const allFilters = [...filterInclude, ...filterExclude];

  const [searchTerm, setSearchTerm] = useState();

  function handleChangeSearchTerm(e) {
    setSearchTerm(e.target.value);
  }

  const props = {
    allNames: filterList({ list: allNames, filter: searchTerm }),
    filterExclude,
    onChange,
    allFilters,
    // filterGroupName,
    searchTerm,
    handleChangeSearchTerm,
  };
  return <Presentation {...props} />;
}
