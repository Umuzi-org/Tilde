import { canSetDueTime } from "./utils";

test("canSetDueTime function returns true if card belongs to current user and there's no due time set", () => {
    const authUser = {id: 1}
    const card = {
        assignees: [authUser.id],
        dueTime: null,
    }
    expect(canSetDueTime({card, authUser})).toBe(true);
});

test("canSetDueTime function returns false if card belongs to current user, user has no special permissions and there is a due time set", () => {
    const authUser = {
        id: 1,
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
        assigneeNames: [authUser.id],
        dueTime: "2021-06-14T09:58:28Z",
    }
    expect(canSetDueTime({card, authUser})).toBe(false);
});

test("canSetDueTime function returns true if current user is not the assigned user but has management permissions and due time is not set", () => {
    const authUser = {
        id: 1,
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
        assigneeNames: [2],
        dueTime: null,
    }
    expect(canSetDueTime({card, authUser})).toBe(true);
});

test("canSetDueTime function returns false if card doesn't belong to current user, current user doesn't have management permissions and there's no due time set", () => {
    const authUser = {
        id: 1,
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
    expect(canSetDueTime({card, authUser})).toBe(false);
});