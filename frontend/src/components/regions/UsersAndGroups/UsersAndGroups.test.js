import { cleanAndFilterTeams } from ".";
import { getPrStatus, getTildeReviewStatus, timeDifferenceInDays } from "./utils"

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

test("getPrStatus should return error when pr age is older than PR_ERROR_AGE_THRESHOLD", () => {
  const oldDate = "2021-10-13T04:45:01Z";
  expect(getPrStatus(oldDate)).toBe("error");
});

test("getPrStatus should return warning when pr age is older than PR_WARNING_AGE_THRESHOLD", () => {
  const getYesterdayDate = new Date();
  getYesterdayDate.setDate(getYesterdayDate.getDate() - 2);
  expect(getPrStatus(getYesterdayDate)).toBe("warning");
});

test("getPrStatus should return default when pr age is younger than PR_WARNING_AGE_THRESHOLD and PR_ERROR_AGE_THRESHOLD", () => {
  const newDate = new Date();
  expect(getPrStatus(newDate)).toBe("default");
});

test("getTildeReviewStatus should return error when tilde review age is older than TILDE_ERROR_AGE_THRESHOLD", () => {
  const oldDate = "2021-10-13T04:45:01Z";
  expect(getTildeReviewStatus(oldDate)).toBe("error");
});

test("getTildeReviewStatus should return warning when tilde review age is less than or equal to TILDE_WARNING_AGE_THRESHOLD", () => {
  const getYesterdayDate = new Date();
  getYesterdayDate.setDate(getYesterdayDate.getDate() - 2);
  expect(getTildeReviewStatus(getYesterdayDate)).toBe("warning");
});

test("getTildeReviewStatus should return default when tilde review age is younger than TILDE_WARNING_AGE_THRESHOLD and TILDE_ERROR_AGE_THRESHOLD", () => {
  const newDate = new Date();
  const hoursAgo = newDate.setHours(newDate.getHours() - 2);
  expect(getTildeReviewStatus(hoursAgo)).toBe("default");
});

test("timeDifferenceInDays should return 5 as the difference between the current date and '5 days ago'", () => {
  const getDate = new Date();
  getDate.setDate(getDate.getDate() - 6);
  expect(timeDifferenceInDays(getDate)).toBe(5);
})