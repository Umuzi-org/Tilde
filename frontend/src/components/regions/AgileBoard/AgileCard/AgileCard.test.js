import { getAgeString } from "../../../widgets/utils";

test("getAgeString function returns correct string when age is 1 month", () => {
    const date = new Date();
    const card = {
        oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 31)
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("1 month ago");
});

test("getAgeString function returns correct string when age is 2 weeks", () => {
    const date = new Date();
    const card = {
        oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 14)
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 weeks ago");
});

test("getAgeString function returns correct string when age is 2 days", () => {
    const date = new Date();
    const card = {
        oldestOpenPrUpdatedTime: date.setDate(date.getDate() - 2)
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 days ago");
});

test("getAgeString function returns correct string when age is 5 hours", () => {
    const date = new Date();
    const card = {
        oldestOpenPrUpdatedTime: date.setHours(date.getHours() - 5)
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("5 hours ago");
});

test("getAgeString function returns correct string when age is 30 minutes", () => {
    const date = new Date();
    const card = {
        oldestOpenPrUpdatedTime: date.setMinutes(date.getMinutes() - 30)
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("30 minutes ago");
});

test("getAgeString function returns correct string when age is less than a minute", () => {
    const date = new Date();
    const card = {
        oldestOpenPrUpdatedTime: date.setSeconds(date.getSeconds() - 15)
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("just now");
});