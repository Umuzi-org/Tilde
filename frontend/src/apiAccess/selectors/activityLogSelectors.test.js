import { getActivityLogCountsByDayForSingleUser } from "./activityLogSelectors";
import {
  ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
  ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
} from "../../constants";

test("getActivityLogCountsByDayForSingleUser calculates correctly", () => {
  const activityLogDayCounts = [
    {
      id:
        "date=2020-04-28&limit=20&offset=0&event_type=5&filter_by_actor_user=236",
      date: "2020-04-28",
      total: 1,
    },
    {
      id:
        "date=2020-04-28&limit=20&offset=0&event_type=5&filter_by_actor_user=2360",
      date: "2020-04-29",
      total: 1,
    },
  ];

  const result = getActivityLogCountsByDayForSingleUser({
    activityLogDayCounts,
    userId: 236,
    eventTypes: [5, 6],
  });

  expect(result).toStrictEqual([
    {
      date: "2020-04-28",
      5: 1,
      6: 0,
    },
  ]);
});
