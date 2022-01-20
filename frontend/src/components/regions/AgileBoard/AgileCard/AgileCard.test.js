import { getAgeString, trimLongReview } from "../../../widgets/utils";
import { userReviewedSinceLastReviewRequest } from "./utils";
import { repoUrlCleaner } from "../../../widgets/utils";

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

test("userReviewedSinceLastReviewRequest should return true if the card is in the review column and the user is part of the latest reviewers", () => {
  const card = {
    status: "IR",
    usersThatReviewedSinceLastReviewRequest: [777, 555, 28, 3332],
  };
  const viewedUser = {
    id: 28,
  };
  expect(userReviewedSinceLastReviewRequest({ viewedUser, card })).toBe(true);
});

test("userReviewedSinceLastReviewRequest should return false if the card is in the review column but the user is not part of the latest reviewers", () => {
  const card = {
    status: "IR",
    usersThatReviewedSinceLastReviewRequest: [777, 555, 3332],
  };
  const viewedUser = {
    id: 28,
  };
  expect(userReviewedSinceLastReviewRequest({ viewedUser, card })).toBe(false);
});

test("git repo url should be cleaned to link to the pull request index on github", () => {
  const gitRepo =
    "git@github.com:Umuzi-org/Nkosinathi-Mtshali-705-contentitem-python.git";
  expect(repoUrlCleaner(gitRepo)).toBe(
    "https://github.com/Umuzi-org/Nkosinathi-Mtshali-705-contentitem-python/pulls"
  );
});

test("A long review should be shortend", () => {
  const longReview =
    "This is a very decriptive, long code review\n that can become hard to read.\n We need to shorten it";
  expect(trimLongReview(longReview)).toBe(
    "This is a very decriptive, long code review"
  );
});
