export function formatTimeString(timestamp) {
  const date = new Date(Date.parse(timestamp));
  return new Intl.DateTimeFormat().format(date);
}

export function getReviewStatus({ review }) {
  return review.state === "changes_requested"
    ? review.state.split("_").join(" ")
    : review.state;
}
