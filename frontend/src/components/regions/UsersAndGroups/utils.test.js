import {
  getPrStatus,
  getTildeReviewStatus,
  timeDifferenceInDays,
  configuration,
  statuses,
} from "./utils";

const {
  PR_ERROR_AGE_THRESHOLD,
  PR_WARNING_AGE_THRESHOLD,
  TILDE_ERROR_AGE_THRESHOLD,
  TILDE_WARNING_AGE_THRESHOLD,
} = configuration;

const { ERROR_STATUS, WARNING_STATUS, DEFAULT_STATUS } = statuses;

test("getPrStatus function returns error string when the pr age is 2 days or older", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(
      date.getDate() - PR_ERROR_AGE_THRESHOLD
    ),
  };
  expect(getPrStatus(card.oldestOpenPrUpdatedTime)).toBe(ERROR_STATUS);
});

test("getPrStatus function returns warning string when the pr age is 1 day or older", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(
      date.getDate() - PR_WARNING_AGE_THRESHOLD
    ),
  };
  expect(getPrStatus(card.oldestOpenPrUpdatedTime)).toBe(WARNING_STATUS);
});

test("getPrStatus function returns default string when the pr age is less than 1 day", () => {
  const date = new Date();
  const card = {
    oldestOpenPrUpdatedTime: date.setDate(date.getDate()),
  };
  expect(getPrStatus(card.oldestOpenPrUpdatedTime)).toBe(DEFAULT_STATUS);
});

test("getTildeReviewStatus function returns error string when the tilde review request age is 3 days or older", () => {
  const date = new Date();
  const card = {
    oldestCardInReviewTime: date.setDate(
      date.getDate() - TILDE_ERROR_AGE_THRESHOLD
    ),
  };
  expect(getTildeReviewStatus(card.oldestCardInReviewTime)).toBe(ERROR_STATUS);
});

test("getTildeReviewStatus function returns warning string when the tilde review request age is 2 days or older", () => {
  const date = new Date();
  const card = {
    oldestCardInReviewTime: date.setDate(
      date.getDate() - TILDE_WARNING_AGE_THRESHOLD
    ),
  };
  expect(getTildeReviewStatus(card.oldestCardInReviewTime)).toBe(
    WARNING_STATUS
  );
});

test("getTildeReviewStatus function returns default string when the tilde review request age is 1 day or less", () => {
  const date = new Date();
  const card = {
    oldestCardInReviewTime: date.setDate(date.getDate()),
  };
  expect(getTildeReviewStatus(card.oldestCardInReviewTime)).toBe(
    DEFAULT_STATUS
  );
});

test("timeDifferenceInDays function should return the correct number of days", () => {
  const date = new Date();
  expect(timeDifferenceInDays(date)).toBe(0);
});
