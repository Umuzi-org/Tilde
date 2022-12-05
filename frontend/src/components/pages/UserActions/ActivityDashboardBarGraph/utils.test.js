import { prepareDataForBarGraph } from "./utils";

test("prepareDataForBarGraph should return an array of objects with unique dates and actions that took place on a particular date", () => {
  const eventTypes = [
    {
      id: 6,
      name: "CARD_MOVED_TO_COMPLETE",
      description: null,
    },
    {
      id: 5,
      name: "CARD_MOVED_TO_REVIEW_FEEDBACK",
      description: null,
    },
    {
      id: 7,
      name: "CARD_REVIEW_REQUEST_CANCELLED",
      description: null,
    },
    {
      id: 4,
      name: "CARD_REVIEW_REQUESTED",
      description: null,
    },
    {
      id: 3,
      name: "CARD_STARTED",
      description: null,
    },
    {
      id: 1,
      name: "COMPETENCE_REVIEW_DONE",
      description: null,
    },
    {
      id: 2,
      name: "PR_REVIEWED",
      description: null,
    },
  ];
  const activityLogDayCounts = [
    {
      id: "date=2022-08-12&event_type=1&filter_by_actor_user=2&filter_by_effected_user=",
      date: "2022-08-12",
      total: 6,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 1,
    },
    {
      id: "date=2022-08-12&event_type=5&filterByActorUser=2&filter_by_effected_user=",
      date: "2022-08-12",
      total: 3,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 5,
    },
    {
      id: "date=2022-08-12&event_type=6&filter_by_actor_user=2&filter_by_effected_user=",
      date: "2022-08-12",
      total: 4,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 6,
    },
    {
      id: "date=2022-08-11&event_type=1&filter_by_actor_user=2&filter_by_effected_user=",
      date: "2022-08-11",
      total: 2,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 1,
    },
    {
      id: "date=2022-08-12&event_type=1&filter_by_actor_user=2&filter_by_effected_user=",
      date: "2022-08-11",
      total: 6,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 2,
    },
    {
      id: "date=2022-08-12&event_type=5&filterByActorUser=2&filter_by_effected_user=",
      date: "2022-08-11",
      total: 3,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 5,
    },
    {
      id: "date=2022-08-12&event_type=5&filterByActorUser=2&filter_by_effected_user=",
      date: "2022-08-10",
      total: 5,
      filterByActorUser: "2",
      filterByEffectedUser: "",
      eventType: 6,
    },
  ];
  const preparedActivityLogDayCountsSample = [
    {
      date: "2022-08-12",
      COMPETENCE_REVIEW_DONE: 6,
      CARD_MOVED_TO_REVIEW_FEEDBACK: 3,
      CARD_MOVED_TO_COMPLETE: 4,
    },
    {
      date: "2022-08-11",
      COMPETENCE_REVIEW_DONE: 2,
      PR_REVIEWED: 6,
      CARD_MOVED_TO_REVIEW_FEEDBACK: 3,
    },
    {
      date: "2022-08-10",
      CARD_MOVED_TO_COMPLETE: 5,
    },
  ];

  const result = prepareDataForBarGraph({ eventTypes, activityLogDayCounts });
  expect(result).toEqual(preparedActivityLogDayCountsSample);
});
