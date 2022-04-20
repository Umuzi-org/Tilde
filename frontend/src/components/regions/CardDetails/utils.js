/*
  The reason markdown is removed from a short review is because we want to keep
  the "summary review" of a long review clean an streamlined (like gmail) - so we 
  return a plain string instead of markdown.
  The clean markdown function attempts to clean the "summary review", leaving it
  markdown free while ignoring common english punctuation marks.
*/

function cleanMarkdown(review) {
  const cleanMarkdownCharacters = review.replace(/[^A-Za-z;!.,:]/gi, " ");
  const cleanRemainingWhiteSpace = cleanMarkdownCharacters.replace(/\s+/g, " ");
  return cleanRemainingWhiteSpace.replace(" . ", " ");
}

export function trimReviewComments(comments) {
  return cleanMarkdown(comments.trim().replace("\n", " ").slice(0, 220));
}
