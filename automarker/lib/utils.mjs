export function dirNameFromRepoUrl({ repoUrl }) {
  const matches = repoUrl.match(/(?<=git@github.com:).*(?=.git)/);
  console.assert(matches.length === 1);
  return matches[0].replace("/", "-");
}
