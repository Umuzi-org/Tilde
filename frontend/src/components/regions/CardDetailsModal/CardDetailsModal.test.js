import { canSetDueTime } from "./utils";

test("canSetDueTime function returns true if card belongs to current user and there's no due time set", () => {
    const authUser = {
        userId: 1,
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
    const card = {
        assignees: [authUser.userId],
        dueTime: null,
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, authUser, teams})).toBe(true);
});

test("canSetDueTime function returns false if card belongs to current user, user has no special permissions and there is a due time set", () => {
    const authUser = {
        userId: 1,
        permissions: {
            teams: {}
        }
    } 
    const card = {
        assignees: [authUser.userId],
        dueTime: "2021-06-14T09:58:28Z",
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, authUser, teams})).toBe(false);
});

test("canSetDueTime function returns true if current user is not the assigned user but has management permissions and due time is not set", () => {
    const authUser = {
        userId: 1,
        email: "babalwa.mbolekwa@umuzi.org",
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
    const card = {
        assignees: [2],
        dueTime: null,
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, authUser, teams})).toBe(true);
});

test("canSetDueTime function returns false if card doesn't belong to current user, current user doesn't have management permissions and there's no due time set", () => {
    const authUser = {
        userId: 1,
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
    const card = {
        assignees: [2],
        dueTime: null,
    }
    const teams = authUser.permissions.teams;
    expect(canSetDueTime({card, authUser, teams})).toBe(false);
});