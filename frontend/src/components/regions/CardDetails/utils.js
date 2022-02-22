/*
  The reason markdown is removed from a short review is because we want to keep
  the "summary review" of a long review clean an streamlined (like gmail) - so we 
  return a plain string instead of markdown.
  The clean markdown function attempts to clean the "summary review", leaving it
  markdown free while ignoring common english puntuation marks.
*/
 
export const cleanMarkdown = (review) => {
  const ignore = review.replace(/[^A-Za-z;!.,:]/gi, " ");
  return ignore.replace("   ", " ").split("  ").join(" ");
}