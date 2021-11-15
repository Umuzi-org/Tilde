export function checkIfCardIsInReviewColumn({ card }) {
  return card.status === "IR";
}

export function userReviewedSinceLastReviewRequest({ viewedUser, card }) {
  return (
    card.usersThatReviewedSinceLastReviewRequest.includes(viewedUser.id);
  );
}
