import { getAgeString } from "../../../widgets/utils";

test("getAgeString function returns correct open pr age string in weeks", () => {
    const card = {
        oldestOpenPrUpdatedTime: "2021-06-14T09:58:28Z"
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 weeks ago");
});

test("getAgeString function returns correct open pr age string in days", () => {
    const card = {
        oldestOpenPrUpdatedTime: "2021-06-27T09:45:28Z"
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 days ago");
});

test("getAgeString function returns correct open pr age string in hours", () => {
    const card = {
        oldestOpenPrUpdatedTime: "2021-06-29T07:49:28Z"
    };
    expect(getAgeString(card.oldestOpenPrUpdatedTime)).toBe("2 hours ago");
});