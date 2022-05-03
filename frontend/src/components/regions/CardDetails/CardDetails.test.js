import { canSetDueTime } from "./utils";

test(`canSetDueTime function returns true if card belongs to current 
        user and there's no due time set`, () => {
  const viewedUser = {
    id: 295,
  };
  const authUser = {
    userId: viewedUser.id,
  };
  const card = {
    assignees: [viewedUser.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, viewedUser, authUser })).toBe(true);
});

test(`canSetDueTime function returns false if card belongs to current user, 
        user has no special permissions and there is a due time set`, () => {
  const viewedUser = {
    id: 295,
  };
  const authUser = {
    userId: viewedUser.id,
  };
  const card = {
    assignees: [viewedUser.id],
    dueTime: "2021-06-14T09:58:28Z",
  };

  expect(canSetDueTime({ card, viewedUser, authUser })).toBe(false);
});

test(`canSetDueTime function returns false if card doesn't belongs to 
        current user and there's no due time set`, () => {
  const viewedUser = {
    id: 295,
  };
  const authUser = {
    userId: 200,
  };
  const card = {
    assignees: [viewedUser.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, viewedUser, authUser })).toBe(false);
});

test(`canSetDueTime function returns true if card doesn't belongs to current user, 
        current user has management permissions and no due time set`, () => {
  const viewedUser = {
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
    assignees: [viewedUser.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, viewedUser, authUser })).toBe(true);
});

test(`canSetDueTime function returns false if card doesn't belong to current user, 
        current user doesn't have management permissions and there's no due time set`, () => {
  const viewedUser = {
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

  expect(canSetDueTime({ card, viewedUser, authUser })).toBe(false);
});

test(`canSetDueTime function returns true for superusers`, () => {
  const viewedUser = {
    id: 295,
    teamMemberships: {
      28: {
        id: 28,
        name: "Cohort 22 web dev",
      },
    },
  };
  const authUser = {
    email: 'sbonelo.mkhize@umuzi.org',
    token: 'c434920a0a10ae0469984f6022bd5ec20f11bf94',
    userId: 2,
    active: true,
    firstName: 'Sbonelo',
    lastName: 'Mkhize',
    preferredName: null,
    isStaff: 1,
    isSuperuser: 1,
    permissions: {
      teams: {
        '1': {
          id: 1,
          name: 'demo team',
          active: true,
          permissions: [
            'MANAGE_CARDS',
            'VIEW_ALL'
          ]
        }
      }
    }
  }
  const card = {
    assignees: [viewedUser.id],
    dueTime: null,
  };

  expect(canSetDueTime({ card, viewedUser, authUser })).toBe(true);
});
