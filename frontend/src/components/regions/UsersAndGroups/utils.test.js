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
  const today = new Date();
  const date = today.setDate(today.getDate() - PR_ERROR_AGE_THRESHOLD)
  expect(getPrStatus(date)).toBe(ERROR_STATUS);
  
});

test("getPrStatus function returns warning string when the pr age is 1 day or older", () => {
  const today = new Date();
  const date = today.setDate(today.getDate() - PR_WARNING_AGE_THRESHOLD)
  expect(getPrStatus(date)).toBe(WARNING_STATUS);
});

test("getPrStatus function returns default string when the pr age is less than 1 day", () => {
  const today = new Date();
  const date = today.setDate(today.getDate())
  expect(getPrStatus(date)).toBe(DEFAULT_STATUS);
});

test("getTildeReviewStatus function returns error string when the tilde review request age is 3 days or older", () => {
  const today = new Date();
  const date = today.setDate(today.getDate() - TILDE_ERROR_AGE_THRESHOLD)
  expect(getTildeReviewStatus(date)).toBe(ERROR_STATUS);
});

test("getTildeReviewStatus function returns warning string when the tilde review request age is 2 days or older", () => {
  const today = new Date();
  const date = today.setDate(today.getDate() - TILDE_WARNING_AGE_THRESHOLD)
  expect(getTildeReviewStatus(date)).toBe(WARNING_STATUS);
});

test("getTildeReviewStatus function returns default string when the tilde review request age is 1 day or less", () => {
  const today = new Date();
  const date = today.setDate(today.getDate())
  expect(getTildeReviewStatus(date)).toBe(DEFAULT_STATUS);
});

test("timeDifferenceInDays function should return the correct number of days", () => {
  const today = new Date();
  expect(timeDifferenceInDays(today)).toBe(0);
});
