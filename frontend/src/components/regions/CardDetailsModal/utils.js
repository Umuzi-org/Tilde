export function canSetDueTime({ card, authUser, teams }) {
    return (
        !card.dueTime && (
            (authUser.id === card.assignees[0]) ||

            (authUser.id !== card.assignees[0] && Object.keys(authUser.permissions.teams)
            .map((key) => authUser.permissions.teams[key].permissions[0]).length !== 0) ||
            
            (authUser.id !== card.assignees[0] && Object.keys(authUser.permissions.teams)
            .map((key) => authUser.permissions.teams[key].permissions[0]).includes("MANAGE_CARDS"))
        )
    )
}