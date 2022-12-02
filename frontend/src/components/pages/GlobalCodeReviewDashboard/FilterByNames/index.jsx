import React, { useState } from "react";
import { filterList } from "../utils";
import Presentation from "./Presentation";

export default function FilterByNames({
  allNames,
  filterInclude,
  filterExclude,
  onChange,
}) {
  allNames = allNames || [];
  filterInclude = filterInclude || [];
  filterExclude = filterExclude || [];
  const allFilters = [...filterInclude, ...filterExclude];

  const [searchTerm, setSearchTerm] = useState("");

  function handleChangeSearchTerm(e) {
    setSearchTerm(e.target.value);
  }

  const props = {
    allNames: filterList({ list: allNames, filter: searchTerm }),
    filterExclude,
    onChange,
    allFilters,
    searchTerm,
    handleChangeSearchTerm,
  };
  return <Presentation {...props} />;
}
