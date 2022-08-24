import { cleanAndFilterTeams, cleanAndFilterUsers } from ".";

const teams = {
  "1": {
    id: 1,
    name: "demo group 1 AAA",
    active: true,
    members: [
      {
        userId: 1,
        userEmail: "sheena.oconnell@umuzi.org",
        permissionStudent: true,
        permissionView: false,
        permissionManage: false,
        userActive: false,
      },
    ],
  },
  2: {
    id: 2,
    name: "demo group 2 aaa",
    active: true,
    members: [
      {
        userId: 1,
        userEmail: "sheena.oconnell@umuzi.org",
        permissionStudent: true,
        permissionView: false,
        permissionManage: false,
        userActive: true,
      },
    ],
  },
};

test("cleanAndFilterTeams can deal with empty filter", () => {
  const ret = cleanAndFilterTeams({ teams, filterBy: "" });

  const names = ret.map((group) => group.name);
  expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
});

test("cleanAndFilterTeams can deal with whitespace filter", () => {
  const ret = cleanAndFilterTeams({ teams, filterBy: "   " });

  const names = ret.map((group) => group.name);
  expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
});

test("cleanAndFilterTeams can deal with upper and lowercase", () => {
  const ret = cleanAndFilterTeams({ teams, filterBy: "aaa" });

  const names = ret.map((group) => group.name);
  expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
});

test("cleanAndFilterTeams can deal with actual differences", () => {
  const ret = cleanAndFilterTeams({ teams, filterBy: "2" });

  const names = ret.map((group) => group.name);
  expect(names).toEqual(["demo group 2 aaa"]);
});

test("cleanAndFilterTeams can deal with multiple words", () => {
  const ret = cleanAndFilterTeams({ teams, filterBy: "demo group" });

  const names = ret.map((group) => group.name);
  expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
});

test("cleanAndFilterTeams can deal with multiple words in any order", () => {
  const ret = cleanAndFilterTeams({ teams, filterBy: "group demo" });

  const names = ret.map((group) => group.name);
  expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
});

test("cleanAndFilterUsers only returns active users", () => {
  const ret = cleanAndFilterUsers(
    teams,
    "sheena.oconnell@umuzi.org",
    "demo group 2 aaa"
  );
  expect(ret).toEqual({
    "sheena.oconnell@umuzi.org": {
      groups: {
        "demo group 2 aaa": {
          permissionManage: false,
          permissionStudent: true,
          permissionView: false,
          teamId: 2,
          userActive: true,
          userEmail: "sheena.oconnell@umuzi.org",
          userId: 1,
        },
      },
      userId: 1,
    },
  });
});

test("cleanAndFilterUsers returns an empty object for deactivated users", () => {
  const ret = cleanAndFilterUsers(
    teams,
    "sheena.oconnell@umuzi.org",
    "demo group 1 AAA"
  );
  expect(ret).toEqual({})
})