
const isCardInReviewColumn = ({ card }) => {
	return card.status === "IR";
}

const checkIfUserIdExistsInReviewers = ({ authUser, card }) => {
	const userId = authUser.id;
	const reviewerList = card.usersThatReviewedSinceLastReviewRequest;
	return reviewerList.includes(userId);
}

export function showCheckedBox({ authUser, card }) {
	return isCardInReviewColumn({ card }) && checkIfUserIdExistsInReviewers({ authUser, card });
}