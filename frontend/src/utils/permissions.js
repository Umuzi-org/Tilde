/* Does the authenticated user have one of the listed permissions on the team */
export function hasPermissionOnTeam({ authUser, teamId, permissions }) {
  //   if (authUser.isSuperuser) return true;
  const teamsWithPermissions = authUser.permissions
    ? authUser.permissions.teams
    : [];

  const permissionsEntry = teamsWithPermissions[teamId];
  if (!permissionsEntry) return false;

  const hasPermission = permissions.filter((value) =>
    permissionsEntry.permissions.includes(value)
  );

  if (hasPermission) return true;
  return false;
}

/* Does the authenticated user have one of the listed permissions on the user */
export function hasPermissionOnUser({ authUser, user, permissions }) {
  //   if (authUser.isSuperuser) return true;
  const teamMemberships = user.teamMemberships
    ? Object.keys(user.teamMemberships)
    : [];

  for (let teamId of teamMemberships) {
    if (hasPermissionOnTeam({ authUser, teamId, permissions })) return true;
  }
  return false;
}
