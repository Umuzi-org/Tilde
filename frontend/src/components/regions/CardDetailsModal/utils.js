export function canSetDueTime({ card, authUser }) {
    return (
        !card.dueTime && authUser.email === card.assigneeNames[0] && 
        Object.keys(authUser.permissions.teams)
        .map((key) => authUser.permissions.teams[key].permissions[0])
        .includes("MANAGE_CARDS") 
    )
}