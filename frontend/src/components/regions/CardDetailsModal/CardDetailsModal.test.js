import { canSetDueTime } from "../../widgets/utils";
import card from "../../../stories/fixtures/agileCard.json";
import authUser from "../../../stories/fixtures/authUser.json";

/* Instance 1: Card belongs to current user and there is no due time set */
test("canSetDueTime function returns true if card belongs to current user and there's no due time set", () => {
    const user = {id: 1}
    const card = {
        assigneeNames: [user.id],
        dueTime: null,
    }
    expect(canSetDueTime({card, user})).toBe(true);
});

/* Instance 2: Card belongs to current user, user has no special permissions and there is a due time set */
test("canSetDueTime function returns false if card belongs to current user, user has no special permissions and there is a due time set", () => {
    const user = {
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
        assigneeNames: [user.id],
        dueTime: "2021-06-14T09:58:28Z",
    }
    expect(canSetDueTime({card, user})).toBe(false);
});

/* Instance 3: Current user is not the assigned user but has management permissions and due time is not set */
test("canSetDueTime function returns true if current user is not the assigned user but has management permissions and due time is not set", () => {
    const user = {
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
        assigneeNames: [user.id],
        dueTime: null,
    }
    expect(canSetDueTime({card, user})).toBe(true);
});

/* Instance 4: Current user is not the assigned user, due time is not set and
   current user doesn't have the 'MANAGE_CARDS' permission */
test("canSetDueTime function returns false if card doesn't belong to current user, current user doesn't have management permissions and there's no due time set", () => {
    expect(canSetDueTime({card, authUser})).toBe(false);
});







