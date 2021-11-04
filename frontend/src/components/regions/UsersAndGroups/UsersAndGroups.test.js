import { cleanAndFilterTeams } from ".";

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
