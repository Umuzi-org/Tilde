
const checkIfCardIsInReviewColumn = ({ card }) => {
	return card.status === "IR";
}
checkIfCardIsInReviewColumn()

const checkIfUserIdExistsInReviewers = ({ authUser, card }) => {
	const userId = authUser.id;
	const reviewerList = card.usersThatReviewedSinceLastReviewRequest;
	return reviewerList.includes(userId);
}

export function showCheckedBox({ authUser, card }) {
	return checkIfCardIsInReviewColumn({ card }) && checkIfUserIdExistsInReviewers({ authUser, card });
}
