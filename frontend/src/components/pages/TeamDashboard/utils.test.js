import { getMinimumAndMaximumValue } from "./utils";
import { updateActivityLogDayCounts } from "./utils";

test("updateActivityLogDayCounts returns updated activityLogDayCounts with same dates", () => {
  const activityLogDayCounts = {
    84: [
      {
        date: "2021-07-14",
        COMPETENCE_REVIEW_DONE: 5,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-19",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 0,
      },
    ],

    26: [
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 5,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 1,
      },
    ],

    132: [
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 50,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 2,
      },
    ],
  };

  const sampleUpdatedActivityLogDayCounts = {
    84: [
      {
        date: "2021-07-14",
        COMPETENCE_REVIEW_DONE: 5,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-19",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 0,
      }
    ],

    26: [
      {
        date: "2021-07-14",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 5,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 1,
      },
      {
        date: "2021-07-19",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      }
    ],

    132: [
      {
        date: "2021-07-14",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 50,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 2,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-19",
        COMPETENCE_REVIEW_DONE: 0,
        PR_REVIEWED: 0,
      }
    ],
  }

  expect(updateActivityLogDayCounts({activityLogDayCounts})).toEqual(sampleUpdatedActivityLogDayCounts);
});

test("getMinimumAndMaximumValue returns the correct minimum and maximum values", () => {
  const activityLogDayCounts = {
    84: [
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 5,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 6,
        PR_REVIEWED: 20,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-18",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-19",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 0,
      },
      {
        date: "2021-07-20",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 0,
      },
    ],

    26: [
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 5,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 6,
        PR_REVIEWED: 2,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 1,
      },
    ],

    132: [
      {
        date: "2021-07-15",
        COMPETENCE_REVIEW_DONE: 50,
        PR_REVIEWED: 3,
      },
      {
        date: "2021-07-16",
        COMPETENCE_REVIEW_DONE: 20,
        PR_REVIEWED: 2,
      },
      {
        date: "2021-07-17",
        COMPETENCE_REVIEW_DONE: 1,
        PR_REVIEWED: 1,
      },
    ],
  };
  const { minValue, maxValue } = getMinimumAndMaximumValue({
    activityLogDayCounts,
  });
  expect(minValue).toBe(0);
  expect(maxValue).toBe(50);
});
