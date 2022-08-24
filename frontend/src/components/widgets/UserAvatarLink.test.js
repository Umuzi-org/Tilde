import { getAvatarTextInitials } from "./UserAvatarLink";

it("getAvatarTextInitials function returns correct initials from an umuzi.org email", () => {
  expect(getAvatarTextInitials("ngoako.ramokgopa@umuzi.org")).toBe("NR");
  expect(getAvatarTextInitials("faith.mofokeng@umuzi.org")).toBe("FM");
});

it("getAvatarTextInitials function returns correct initials from other emails", () => {
  expect(getAvatarTextInitials("projectlkh63@gmail.com")).toBe("PR");
  expect(getAvatarTextInitials("c.nyatondo@gmail.com")).toBe("NY");
  expect(getAvatarTextInitials("n0606160@gmail.com")).toBe(null);
  expect(getAvatarTextInitials("08606160@gmail.com")).toBe(null);
});
