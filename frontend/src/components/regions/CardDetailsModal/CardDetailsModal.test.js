import { canSetDueTime } from "../../widgets/utils";
import card from "../../../stories/fixtures/agileCard.json";
import authUser from "../../../stories/fixtures/authUser.json";

/* Instance 1: Card belongs to current user and there is no due time set */
const cardAndUserObject1 = {
    agileCard: {
        assigneeNames: ["babalwa.mbolekwa@umuzi.org"],
        dueTime: null,
    },
    currentUser: {
        email: "babalwa.mbolekwa@umuzi.org",
    }
}

test("canSetDueTime function returns true if card belongs to current user and there's no due time set", () => {
    expect(canSetDueTime(cardAndUserObject1.agileCard, cardAndUserObject1.currentUser)).toBe(true);
});

/* Instance 2: Card belongs to current user, user has no special permissions and there is a due time set */
const cardAndUserObject2 = {
    agileCard: {
        assigneeNames: ["babalwa.mbolekwa@umuzi.org"],
        dueTime: "2021-06-14T09:58:28Z",
    },
    currentUser: {
        email: "babalwa.mbolekwa@umuzi.org",
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
}

test("canSetDueTime function returns false if card belongs to current user, user has no special permissions and there is a due time set", () => {
    expect(canSetDueTime(cardAndUserObject2.agileCard, cardAndUserObject2.currentUser)).toBe(false);
});

/* Instance 3: Current user is not the assigned user but has management permissions and due time is not set */
const cardAndUserObject3 = {
    agileCard: {
        assigneeNames: ["babalwa.mbolekwa@umuzi.org"],
        dueTime: null,
    },
    currentUser: {
        email: "sheena.oconnell@umuzi.org",
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
}

test("canSetDueTime function returns true if current user is not the assigned user but has management permissions and due time is not set", () => {
    expect(canSetDueTime(cardAndUserObject3.agileCard, cardAndUserObject3.currentUser)).toBe(true);
});

/* Instance 4: Current user is not the assigned user, due time is not set and
   current user doesn't have the 'MANAGE_CARDS' permission */
const cardAndUserObject4 = {
    agileCard: card,
    currentUser: authUser,
}

test("canSetDueTime function returns false if card doesn't belong to current user, current user doesn't have management permissions and there's no due time set", () => {
    expect(canSetDueTime(cardAndUserObject4.agileCard, cardAndUserObject4.currentUser)).toBe(false);
});







