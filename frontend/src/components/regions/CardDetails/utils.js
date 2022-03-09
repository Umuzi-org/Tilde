function userHasPermissionsToManageCards({ authUser, user }) {

  const teamMemberships = user.teamMemberships
    ? Object.keys(user.teamMemberships)
    : [];
  const teams = authUser.permissions ? authUser.permissions.teams : [];
  for (let teamId of teamMemberships) {
    const teamPermissions = teams[teamId] ? teams[teamId].permissions : [];
    if (teamPermissions.includes("MANAGE_CARDS")) {
      return true;
    }
  }
  return false;
}

export function canSetDueTime({ card, user, authUser }) {
  
  if (user.id === authUser.userId && card.dueTime === null) {
    return true;
  }
  if (userHasPermissionsToManageCards({ user, authUser })) {
    return true;
  }
  return false;
}
