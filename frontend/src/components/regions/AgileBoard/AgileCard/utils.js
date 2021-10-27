// To be used later once viro agree's on the ui
const isCardInReviewColumn = ({ card }) => {
	return card.status === "IR";
}

const checkIfUserIdExistsInReviewers = ({ user, card }) => {
	const userId = user.id;
	const reviewerList = card.usersThatReviewedSinceLastReviewRequest;
	return reviewerList.includes(userId);
}

export function showCheckedBox({ user, card }) {
	return isCardInReviewColumn({ card }) && checkIfUserIdExistsInReviewers({ user, card });
}