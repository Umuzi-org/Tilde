import { dirNameFromRepoUrl } from "./utils.mjs";

test("dirNameFromRepoUrl cleans up valid urls", () => {
  expect(
    dirNameFromRepoUrl({ repoUrl: "git@github.com:Umuzi-org/Tilde.git" })
  ).toBe("Umuzi-org-Tilde");
});

TODO;
