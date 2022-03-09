import { canSetDueTime } from "./utils";

test(`canSetDueTime function returns true if card belongs to current 
        user and there's no due time set`, () => {
  const user = {
    id: 295,
  };
  const authUser = {
    userId: user.id,
  };
  const card = {
    assignees: [user.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, user, authUser })).toBe(true);
});

test(`canSetDueTime function returns false if card belongs to current user, 
        user has no special permissions and there is a due time set`, () => {
  const user = {
    id: 295,
  };
  const authUser = {
    userId: user.id,
  };
  const card = {
    assignees: [user.id],
    dueTime: "2021-06-14T09:58:28Z",
  };

  expect(canSetDueTime({ card, user, authUser })).toBe(false);
});

test(`canSetDueTime function returns false if card doesn't belongs to 
        current user and there's no due time set`, () => {
  const user = {
    id: 295,
  };
  const authUser = {
    userId: 200,
  };
  const card = {
    assignees: [user.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, user, authUser })).toBe(false);
});

test(`canSetDueTime function returns true if card doesn't belongs to current user, 
        current user has management permissions and no due time set`, () => {
  const user = {
    id: 295,
    teamMemberships: {
      28: {
        id: 28,
        name: "Cohort 22 web dev",
      },
    },
  };
  const authUser = {
    userId: 200,
    permissions: {
      teams: {
        28: {
          id: 28,
          name: "Cohort 22 web dev",
          active: true,
          permissions: ["MANAGE_CARDS"],
        },
      },
    },
  };
  const card = {
    assignees: [user.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, user, authUser })).toBe(true);
});

test(`canSetDueTime function returns false if card doesn't belong to current user, 
        current user doesn't have management permissions and there's no due time set`, () => {
  const user = {
    id: 295,
    teamMemberships: {
      28: {
        id: 28,
        name: "Cohort 22 web dev",
      },
    },
  };
  const authUser = {
    userId: 200,
    permissions: {
      teams: {
        28: {
          id: 28,
          name: "Cohort 22 web dev",
          active: true,
          permissions: ["REVIEW_CARDS"],
        },
      },
    },
  };
  const card = {
    assignees: [authUser.userId],
    dueTime: null,
  };

  expect(canSetDueTime({ card, user, authUser })).toBe(false);
});
