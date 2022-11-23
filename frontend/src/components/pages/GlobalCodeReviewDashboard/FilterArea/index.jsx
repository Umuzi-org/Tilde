import React from "react";
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
  };
  return <Presentation {...props} />;
}
