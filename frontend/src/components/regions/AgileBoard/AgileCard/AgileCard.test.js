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

test("git repo url should be cleaned to link to the pull request index on github", () => {
  const gitRepo =
    "git@github.com:Umuzi-org/Nkosinathi-Mtshali-705-contentitem-python.git";
  expect(repoUrlCleaner(gitRepo)).toBe(
    "https://github.com/Umuzi-org/Nkosinathi-Mtshali-705-contentitem-python/pulls"
  );
});