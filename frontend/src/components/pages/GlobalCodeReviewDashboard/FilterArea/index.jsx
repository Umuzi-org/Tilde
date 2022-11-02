import React, { useState } from "react";
import Presentation from "./Presentation";

function filterByFilterGroup({ allFilters, filter }) {
  if (filter) {
    return allFilters.filter((card) =>
      card.toLowerCase().includes(filter.toLowerCase())
    );
  }
  return allFilters;
}

export default function FilterArea({
  filterIncludeTags,
  filterExcludeTags,
  filterIncludeFlavours,
  filterExcludeFlavours,
  handleChangeFlavourFilter,
  handleChangeTagFilter,
  allTagNames,
  allFlavours,
  allTeamNames,
  filterIncludeAssigneeTeams,
  handleChangeAssigneeTeamFilter,
  cardNameSearchValue,
  handleChangeCardNameSearchValue,
}) {
  const [flavourSearchTerm, setFlavourSearchTerm] = useState("");
  const [tagSearchTerm, setTagSearchTerm] = useState("");
  const [assigneeTeamSearchTerm, setAssigneeTeamSearchTerm] = useState("");

  function handleChangeSearchTerm({ e, setSearchTermMethod }) {
    setSearchTermMethod(e.target.value);
  }

  const props = {
    filterIncludeTags,
    filterExcludeTags,

    filterIncludeFlavours,
    filterExcludeFlavours,

    handleChangeFlavourFilter,
    handleChangeTagFilter,

    allTagNames,
    allFlavours,
    allTeamNames,
    filterIncludeAssigneeTeams,
    handleChangeAssigneeTeamFilter,

    cardNameSearchValue,
    handleChangeCardNameSearchValue,

    handleChangeSearchTerm,
    flavourSearchTerm,
    setFlavourSearchTerm,
    tagSearchTerm,
    setTagSearchTerm,
    assigneeTeamSearchTerm,
    setAssigneeTeamSearchTerm,
    filterByFilterGroup,
  };
  return <Presentation {...props} />;
}
