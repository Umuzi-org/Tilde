import { getAgeString, repoUrlCleaner } from "./utils";

test("getAgeString function doesn't break if null date", () => {
  expect(getAgeString(null)).toBe("");
  expect(getAgeString(undefined)).toBe("");
});

test("getAgeString function returns correct string when age is 1 month", () => {
  const today = new Date();
  const date = today.setDate(today.getDate() - 31);
  expect(getAgeString(date)).toBe("1 month ago");
});

test("getAgeString function returns correct string when age is 2 weeks", () => {
  const today = new Date();
  const date = today.setDate(today.getDate() - 14);
  expect(getAgeString(date)).toBe("2 weeks ago");
});

test("getAgeString function returns correct string when age is 2 days", () => {
  const today = new Date();
  const date = today.setDate(today.getDate() - 2);
  expect(getAgeString(date)).toBe("2 days ago");
});

test("getAgeString function returns correct string when age is 5 hours", () => {
  const today = new Date();
  const date = today.setHours(today.getHours() - 5);
  expect(getAgeString(date)).toBe("5 hours ago");
});

test("getAgeString function returns correct string when age is 30 minutes", () => {
  const today = new Date();
  const date = today.setMinutes(today.getMinutes() - 30);
  expect(getAgeString(date)).toBe("30 minutes ago");
});

test("getAgeString function returns correct string when age is less than a minute", () => {
  const today = new Date();
  const date = today.setSeconds(today.getSeconds() - 15);
  expect(getAgeString(date)).toBe("just now");
});

// repoUrlCleaner tests
test("git repo url should be cleaned to link to the pull request index on github", () => {
  const gitRepo =
    "git@github.com:Umuzi-org/Nkosinathi-Mtshali-705-contentitem-python.git";
  expect(repoUrlCleaner(gitRepo)).toBe(
    "https://github.com/Umuzi-org/Nkosinathi-Mtshali-705-contentitem-python/pulls"
  );
});

test("git repo should not be only restricted to Umuz owned repositories", () => {
  const gitRepo = "git@github.com:Sbonelo01/personal-portfolio.git";
  expect(repoUrlCleaner(gitRepo)).toBe(
    "https://github.com/Sbonelo01/personal-portfolio/pulls"
  );
});
