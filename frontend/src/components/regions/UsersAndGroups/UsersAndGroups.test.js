import { cleanAndFilterTeams } from ".";
import { getPrColor, getTildeReviewColor } from "./utils"

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
const palette = {
  warning: "#ff9800",
  error: "#ef5350",
  default: "#212121",
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

test("getPrColor should return a black text whenever an oldest pull request is made 'just now'", () => {
  const newDate = new Date();
  expect(getPrColor(newDate)).toBe(palette.default);
});

test("getPrColor should return a red text whenever an oldest pull request is older than two days", () => {
  const oldDate = "2021-10-13T04:45:01Z";
  expect(getPrColor(oldDate)).toBe(palette.error);
});

test("getTildeReviewColor should return a black text whenever an oldest tilde review request is made 'just now'", () => {
  const newDate = new Date();
  expect(getTildeReviewColor(newDate)).toBe(palette.default);
});

test("getTildeReviewColor should return a red text whenever an oldest tilde review request is older than three days", () => {
  const oldDate = "2021-10-13T04:45:01Z";
  expect(getTildeReviewColor(oldDate)).toBe(palette.error);
});