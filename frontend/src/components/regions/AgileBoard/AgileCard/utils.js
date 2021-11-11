export function checkIfCardIsInReviewColumn({ card }) {
  return card.status === "IR";
}

const checkIfUserIdExistsInReviewers = ({ viewedUser, card }) => {
  return card.usersThatReviewedSinceLastReviewRequest.includes(viewedUser.id);
};

export function showCheckedBox({ viewedUser, card }) {
  return (
    checkIfCardIsInReviewColumn({ card }) &&
    checkIfUserIdExistsInReviewers({ viewedUser, card })
  );
}
