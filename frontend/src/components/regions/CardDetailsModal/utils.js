export function canSetDueTime({ card, authUser, teams }) {

    return (
        !card.dueTime && (
            (authUser.userId === card.assignees[0]) ||
            
            (authUser.userId !== card.assignees[0] && 
                Object.keys(teams).map((key) => teams[key].permissions[0]).includes("MANAGE_CARDS"))
        )
    )
}