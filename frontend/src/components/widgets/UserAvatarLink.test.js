import { getAvatarTextInitials } from "./UserAvatarLink";

test("getAvatarTextInitials function returns correct initials from an umuzi.org email", () => {
  expect(getAvatarTextInitials("ngoako.ramokgopa@umuzi.org")).toBe("NR");
  expect(getAvatarTextInitials("faith.mofokeng@umuzi.org")).toBe("FM");
});
test("getAvatarTextInitials function returns correct initials from other emails", () => {
  expect(getAvatarTextInitials("projectlkh63@gmail.com")).toBe("PR");
  expect(getAvatarTextInitials("nn0606160@gmail.com")).toBe("NN");
  expect(getAvatarTextInitials("c.nyatondo@gmail.com")).toBe("NY");
});
