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

test("getPrStatus function returns error string when the pr age is 2 days or older", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 3),
  };
  expect(getPrStatus(card.oldestOpenPrUpdatedTime)).toBe("error");
});

test("getPrStatus function returns warning string when the pr age is 1 day or older", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 2),
  };
  expect(getPrStatus(card.oldestOpenPrUpdatedTime)).toBe("warning");
});

test("getPrStatus function returns default string when the pr age is less than 1 day", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate()),
  };
  expect(getPrStatus(card.oldestOpenPrUpdatedTime)).toBe("default");
});

test("getTildeReviewStatus function returns error string when the tilde review request age is 3 days or older", () => {
  const date = new Date();
  const card = {
    oldestCardInReviewTime: date.setDate(date.getDate() - 4)
  };
  expect(getTildeReviewStatus(card.oldestCardInReviewTime)).toBe("error");
});

test("getTildeReviewStatus function returns warning string when the tilde review request age is 2 days or older", () => {
  const date = new Date();
  const card = {
    oldestCardInReviewTime: date.setDate(date.getDate() - 3)
  };
  expect(getTildeReviewStatus(card.oldestCardInReviewTime)).toBe("warning");
});

test("getTildeReviewStatus function returns default string when the tilde review request age is 1 day or less", () => {
  const date = new Date();
  const card = {
    oldestCardInReviewTime: date.setDate(date.getDate())
  };
  expect(getTildeReviewStatus(card.oldestCardInReviewTime)).toBe("default");
});

test("timeDifferenceInDays function should return 5 as the difference between the current date and '5 days ago'", () => {
  const getDate = new Date();
  getDate.setDate(getDate.getDate() - 6);
  expect(timeDifferenceInDays(getDate)).toBe(5);
})