import { trimLongReview } from "./utils";

test("A long review should be shortend", () => {
  const longReview =
    "This is a very decriptive, long code review\n that can become hard to read.\n We need to shorten it";
  expect(trimLongReview(longReview)).toBe(
    "This is a very decriptive, long code review that can become hard to read. We need to shorten it"
  );
});
