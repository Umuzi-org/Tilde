export function canSetDueTime({ card, user, teams }) {

    return (
        !card.dueTime && (
            (user.id === card.assignees[0]) ||
            
            (user.id !== card.assignees[0] && 
                Object.keys(teams).map((key) => teams[key].permissions[0]).includes("MANAGE_CARDS"))
        )
    )
}