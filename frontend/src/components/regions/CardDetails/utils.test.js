import { trimReviewComments } from "./utils";

test("trimReviewComments should clean a review with markdown", () => {
  const reviewWithMarkup =
    "This is a review! with\n > characters *that one might use when #making a review*";
  expect(trimReviewComments(reviewWithMarkup)).toBe(
    "This is a review! with characters that one might use when making a review "
  );
});

test("trimReviewComments should ignore cleaning some special characters", () => {
  const reviewWithSpecialChars =
    "This! \n is a review with common english punctuation.";
  expect(trimReviewComments(reviewWithSpecialChars)).toBe(
    "This! is a review with common english punctuation."
  );
});

test("trimReviewComments should ignore cleaning some special english punctuation characters", () => {
  const reviewWithSpecialChars =
    "This \n is a review with common english punctuation. We want to \nclean it now";
  expect(trimReviewComments(reviewWithSpecialChars)).toBe(
    "This is a review with common english punctuation. We want to clean it now"
  );
});