import { getAvatarInitials } from "./UserAvatarLink";

it("getAvatarInitials function returns correct initials from an umuzi.org email", () => {
  expect(getAvatarInitials("ngoako.ramokgopa@umuzi.org")).toBe("NR");
  expect(getAvatarInitials("faith.mofokeng@umuzi.org")).toBe("FM");
});

it("getAvatarInitials function returns correct initials from other emails", () => {
  expect(getAvatarInitials("projectlkh63@gmail.com")).toBe("PR");
  expect(getAvatarInitials("c.nyatondo@gmail.com")).toBe("CN");
  expect(getAvatarInitials("n0606160@gmail.com")).toBe("N0");
  expect(getAvatarInitials("08606160@gmail.com")).toBe("08");
});
