import { repoUrlCleaner, getAgeString, filterUsers } from "./utils";

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

test("git repo url should be able to direct to pull request index' of any individually owned repositories", () => {
  const gitRepo1 = "git@github.com:Sbonelo01/personal-portfolio.git";
  expect(repoUrlCleaner(gitRepo1)).toBe(
    "https://github.com/Sbonelo01/personal-portfolio/pulls"
  );
});

test("git repo url should be able to direct to pull request index' of any external organizations repositories", () => {
  const gitRepo2 = "git@github.com:facebook/react.git";
  expect(repoUrlCleaner(gitRepo2)).toBe(
    "https://github.com/facebook/react/pulls"
  );
});

test("filterUsers should filter allUsers and keep users who have reviewed and those who are assigned on the card", () => {
  const allUsers = [
    {
      userId: 5,
      email: "joshua.ritson@umuzi.org",
    },
    {
      userId: 185,
      email: "kaleem.mohammad@umuzi.org",
    },
    {
      userId: "ngoako.ramokgopa@umuzi.org",
      email: "ngoako.ramokgopa@umuzi.org",
    },
    {
      userId: 739,
      email: "philasande.ngcamu@umuzi.org",
    },
    {
      userId: "philasande.ngcamu@umuzi.org",
      email: "philasande.ngcamu@umuzi.org",
    },
    {
      userId: 962,
      email: "rmawina@gmail.com",
    },
    {
      userId: "rmawina@gmail.com",
      email: "rmawina@gmail.com",
    },
    {
      userId: 26,
      email: "sbonelo.mkhize@umuzi.org",
    },
    {
      userId: "sbonelo.mkhize@umuzi.org",
      email: "sbonelo.mkhize@umuzi.org",
    },
    {
      userId: 786,
      email: "sinenhlanhla.magubane@umuzi.org",
    },
    {
      userId: "sinenhlanhla.magubane@umuzi.org",
      email: "sinenhlanhla.magubane@umuzi.org",
    },
    {
      userId: 1084,
      email: "tasneem.titus@umuzi.org",
    },
    {
      userId: "tasneem.titus@umuzi.org",
      email: "tasneem.titus@umuzi.org",
    },
    {
      userId: 891,
      email: "vuyisanani.meteni@umuzi.org",
    },
  ];
  const filteredUsers = [
    {
      userId: 5,
      email: "joshua.ritson@umuzi.org",
    },
    {
      userId: 185,
      email: "kaleem.mohammad@umuzi.org",
    },
    {
      userId: "philasande.ngcamu@umuzi.org",
      email: "philasande.ngcamu@umuzi.org",
    },
    {
      userId: "rmawina@gmail.com",
      email: "rmawina@gmail.com",
    },
    {
      userId: "sbonelo.mkhize@umuzi.org",
      email: "sbonelo.mkhize@umuzi.org",
    },
    {
      userId: "sinenhlanhla.magubane@umuzi.org",
      email: "sinenhlanhla.magubane@umuzi.org",
    },
    {
      userId: "tasneem.titus@umuzi.org",
      email: "tasneem.titus@umuzi.org",
    },
    {
      userId: 891,
      email: "vuyisanani.meteni@umuzi.org",
    },
    {
      userId: "ngoako.ramokgopa@umuzi.org",
      email: "ngoako.ramokgopa@umuzi.org",
    },
  ];
  expect(filterUsers(allUsers)).toStrictEqual(filteredUsers);
});
