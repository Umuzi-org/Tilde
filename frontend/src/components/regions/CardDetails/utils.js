function userHasPermissionsToManageCards({ authUser, viewedUser }) {
  const teamMemberships = viewedUser.teamMemberships
    ? Object.keys(viewedUser.teamMemberships)
    : [];
  const teams = authUser.permissions ? authUser.permissions.teams : [];
  for (let teamId of teamMemberships) {
    const teamPermissions = teams[teamId] ? teams[teamId].permissions : [];
    if (teamPermissions.includes("MANAGE_CARDS") || authUser.isSuperuser) {
      return true;
    }
  }
  return false;
}

export function canSetDueTime({ card, viewedUser, authUser }) {
  if (viewedUser.id === authUser.userId && card.dueTime === null) {
    return true;
  }
  if (userHasPermissionsToManageCards({ viewedUser, authUser })) {
    return true;
  }
  return false;
}
