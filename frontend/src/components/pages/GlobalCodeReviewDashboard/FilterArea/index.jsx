import React, { useState } from "react";
import Presentation from "./Presentation";

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
  };
  return <Presentation {...props} />;
}
