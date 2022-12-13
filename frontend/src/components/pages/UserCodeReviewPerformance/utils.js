export function formatTimeString(timestamp) {
  const date = new Date(Date.parse(timestamp));
  return new Intl.DateTimeFormat().format(date);
}

export function getReviewStatus({ review }) {
  if (review.state === "changes_requested") {
    return "changes requested";
  }
  return review.state;
}
