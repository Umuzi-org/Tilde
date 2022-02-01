import { getMinAndMaxDate } from "./utils";

test("getMinAndMaxDate returns the correct minimum and maximum dates", () => {
  const activityLogDayCounts = [
    {
      id:
        "date=2020-04-28&limit=20&offset=0&event_type__name=COMPETENCE_REVIEW_DONE&actor_user=236",
      date: "2020-04-28",
      total: 1,
    },
    {
      id:
        "date=2020-04-28&limit=20&offset=0&event_type__name=COMPETENCE_REVIEW_DONE&actor_user=2360",
      date: "2020-04-29",
      total: 1,
    },
    {
      id:
        "date=2020-04-28&limit=20&offset=0&event_type__name=COMPETENCE_REVIEW_DONE&actor_user=2360",
      date: "2021-04-29",
      total: 1,
    },
  ];

  const { minimumDate, maximumDate } = getMinAndMaxDate({
    activityLogDayCounts,
  });
  expect(minimumDate).toBe("2020-04-28");
  expect(maximumDate).toBe("2021-04-29");
});
