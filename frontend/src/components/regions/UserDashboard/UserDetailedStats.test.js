import { fillColor } from "./utils";
import { cardColors } from "../../../colors";

test("fillColor function returns a grey colour for Blocked column", () => {
    const columnName = "Blocked (5)";
    expect(fillColor(columnName)).toBe(cardColors.B);
});

test("fillColor function returns a blue colour for Ready column", () => {
    const columnName = "Ready (2)";
    expect(fillColor(columnName)).toBe(cardColors.R);
});

test("fillColor function returns a green colour for In Progress column", () => {
    const columnName = "In Progress (4)";
    expect(fillColor(columnName)).toBe(cardColors.IP);
});

test("fillColor function returns a red colour for Review Feedback column", () => {
    const columnName = "Review Feedback (3)";
    expect(fillColor(columnName)).toBe(cardColors.RF);
});

test("fillColor function returns a orange colour for Review column", () => {
    const columnName = "Review (5)";
    expect(fillColor(columnName)).toBe(cardColors.IR);
});

test("fillColor function returns a yellow colour for Complete column", () => {
    const columnName = "Complete (81)";
    expect(fillColor(columnName)).toBe(cardColors.C);
});