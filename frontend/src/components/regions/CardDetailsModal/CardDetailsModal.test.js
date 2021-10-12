import { canSetDueTime } from "./utils";

test("canSetDueTime function returns true if card belongs to current user and there's no due time set", () => {
    const authUser = {
        permissions: {
            teams: {
                28: {
                    id: 28,
                    name: "Cohort 22 web dev",
                    active: true,
                    permissions: [
                        "REVIEW_CARDS"
                    ]
                }
            }
        }
    }
    const user = {
        id: 295,
    }
    const card = {
        assignees: [user.id],
        dueTime: null,
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, user, teams})).toBe(true);
});

test("canSetDueTime function returns false if card belongs to current user, user has no special permissions and there is a due time set", () => {
    const authUser = {
        permissions: {
            teams: {}
        }
    } 
    const user = {
        id: 295,
    }
    const card = {
        assignees: [user.id],
        dueTime: "2021-06-14T09:58:28Z",
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, user, teams})).toBe(false);
});

test("canSetDueTime function returns true if current user is not the assigned user but has management permissions and due time is not set", () => {
    const authUser = {
        permissions: {
            teams: {
                28: {
                    id: 28,
                    name: "Cohort 22 web dev",
                    active: true,
                    permissions: [
                        "MANAGE_CARDS"
                    ]
                }
            }
        }
    }
    const user = {
        id: 295,
    }
    const card = {
        assignees: [292],
        dueTime: null,
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, user, teams})).toBe(true);
});

test("canSetDueTime function returns false if card doesn't belong to current user, current user doesn't have management permissions and there's no due time set", () => {
    const authUser = {
        permissions: {
            teams: {
                28: {
                    id: 28,
                    name: "Cohort 22 web dev",
                    active: true,
                    permissions: [
                        "REVIEW_CARDS"
                    ]
                }
            }
        }
    } 
    const user = {
        id: 295,
    }
    const card = {
        assignees: [200],
        dueTime: null,
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, user, teams})).toBe(false);
});