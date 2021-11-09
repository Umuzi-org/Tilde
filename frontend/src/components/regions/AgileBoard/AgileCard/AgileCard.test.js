import { getAgeString } from "../../../widgets/utils";
import { showCheckedBox } from "./utils";

test("getAgeString function doesn't break if null date", () => {
  expect(getAgeString(null)).toBe("");
  expect(getAgeString(undefined)).toBe("");
});

test("getAgeString function returns correct string when age is 1 month", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 31),
  };
  expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("1 month ago");
});

test("getAgeString function returns correct string when age is 2 weeks", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 14),
  };
  expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 weeks ago");
});

test("getAgeString function returns correct string when age is 2 days", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 2),
  };
  expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 days ago");
});

test("getAgeString function returns correct string when age is 5 hours", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setHours(date.getHours() - 5),
  };
  expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("5 hours ago");
});

test("getAgeString function returns correct string when age is 30 minutes", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setMinutes(date.getMinutes() - 30),
  };
  expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("30 minutes ago");
});

test("getAgeString function returns correct string when age is less than a minute", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setSeconds(date.getSeconds() - 15),
  };
  expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("just now");
});

test("showCheckedBox should return true if the card is in the review column and the user is part of the latest reviewers", () => {
  const card = {
    status: "IR",
    reviewers: [777, 555, 28, 3332],
  }
  const viewedUser = {
    id: 28,
  }
  expect(showCheckedBox({ viewedUser, card })).toBe(true)
})

test("showCheckedBox should return false if the card is in the review column but the user is not part of the latest reviewers", () => {
  const card = {
    status: "IR",
    reviewers: [777, 555, 3332],
  }
  const viewedUser = {
    id: 28,
  }
  expect(showCheckedBox({ viewedUser, card })).toBe(false)
})

test("showCheckedBox should return false if the card is not in the review column", () => {
  const card = {
    status: "IP",
  }
  const viewedUser = {
    id: 28,
  }
  expect(showCheckedBox({ viewedUser, card })).toBe(false)
})
