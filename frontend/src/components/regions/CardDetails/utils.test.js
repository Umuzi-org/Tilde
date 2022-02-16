import { trimLongReview, cleanMarkdown } from "./utils";

test("A long review should be shortend", () => {
  const longReview =
    "This is a very decriptive, long code review\nthat can become hard to read.\n We need to shorten it";
  expect(trimLongReview(longReview)).toBe(
    "This is a very decriptive, long code review that can become hard to read.  We need to shorten it"
  );
});

test("A review with markdown should be cleaned", () => {
  const reviewWithMarkup =
    "This is a review! with\n > characters *that one might use when #making a review*";
  expect(cleanMarkdown(trimLongReview(reviewWithMarkup))).toBe(
    "This is a review! with  characters that one might use when making a review "
  );
});

test("Some special characters should be ignored", () => {
  const reviewWithSpecialChars =
    "This! is a review with common english puntuation.";
  expect(cleanMarkdown(trimLongReview(reviewWithSpecialChars))).toBe(
    "This! is a review with common english puntuation."
  );
});
