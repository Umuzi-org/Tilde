import { userReviewedSinceLastReviewRequest } from "./utils";
import { repoUrlCleaner } from "../../../widgets/utils";

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
