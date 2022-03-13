import {trimReviewComments } from "./utils";

test("A review with markdown should be cleaned", () => {
  const reviewWithMarkup =
    "This is a review! with\n > characters *that one might use when #making a review*";
  expect(trimReviewComments(reviewWithMarkup)).toBe(
    "This is a review! with characters that one might use when making a review "
  );
});

test("Some special characters should be ignored", () => {
  const reviewWithSpecialChars =
    "This! \n is a review with common english puntuation.";
  expect(trimReviewComments(reviewWithSpecialChars)).toBe(
    "This! is a review with common english puntuation."
  );
});

test("Some special characters should be ignored", () => {
  const reviewWithSpecialChars =
    "This \n is a review with common english puntuation. We want to \nclean it now";
  expect(trimReviewComments(reviewWithSpecialChars)).toBe(
    "This is a review with common english puntuation. We want to clean it now"
  );
});