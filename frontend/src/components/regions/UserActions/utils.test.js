import {
  fillInSnapshotDateGaps,
  removeDuplicateDates,
  addEventColorsToLogEntries,
} from "./utils";
test("fillInSnapshotDateGaps returns updated burnDownSnapshots with gap dates filled", () => {
  const burnDownSnapshots = [
    {
      timestamp: "2022-04-10",
      total: 5,
    },
    {
      timestamp: "2022-04-15",
      total: 10,
    },
    {
      timestamp: "2022-04-16",
      total: 15,
    },
    {
      timestamp: "2022-04-17",
      total: 20,
    },
    {
      timestamp: "2022-04-18",
      total: 25,
    },
    {
      timestamp: "2022-04-19",
      total: 30,
    },
  ];
  const sampleUpdatedBurnDownSnapshots = [
    {
      timestamp: "2022-04-10",
      total: 5,
    },
    {
      timestamp: "2022-04-11",
      total: 5,
    },
    {
      timestamp: "2022-04-12",
      total: 5,
    },
    {
      timestamp: "2022-04-13",
      total: 5,
    },
    {
      timestamp: "2022-04-14",
      total: 5,
    },
    {
      timestamp: "2022-04-15",
      total: 10,
    },
    {
      timestamp: "2022-04-16",
      total: 15,
    },
    {
      timestamp: "2022-04-17",
      total: 20,
    },
    {
      timestamp: "2022-04-18",
      total: 25,
    },
    {
      timestamp: "2022-04-19",
      total: 30,
    },
  ];
  const result = fillInSnapshotDateGaps({ burnDownSnapshots });
  expect(result).toEqual(sampleUpdatedBurnDownSnapshots);
});

test("removeDuplicateDates returns updated burnDownSnapshots with duplicate dates removed", () => {
  const burnDownSnapshots = [
    {
      timestamp: "2022-04-10",
      total: 5,
    },
    {
      timestamp: "2022-04-15",
      total: 10,
    },
    {
      timestamp: "2022-04-16",
      total: 15,
    },
    {
      timestamp: "2022-04-17",
      total: 20,
    },
    {
      timestamp: "2022-04-18",
      total: 25,
    },
    {
      timestamp: "2022-04-19",
      total: 35,
    },
    {
      timestamp: "2022-04-19",
      total: 35,
    },
  ];
  const sampleUpdatedBurnDownSnapshots = [
    {
      timestamp: "2022-04-10",
      total: 5,
    },
    {
      timestamp: "2022-04-15",
      total: 10,
    },
    {
      timestamp: "2022-04-16",
      total: 15,
    },
    {
      timestamp: "2022-04-17",
      total: 20,
    },
    {
      timestamp: "2022-04-18",
      total: 25,
    },
    {
      timestamp: "2022-04-19",
      total: 35,
    },
  ];
  const result = removeDuplicateDates({ burnDownSnapshots });
  expect(result).toEqual(sampleUpdatedBurnDownSnapshots);
});

test("fillInSnapshotDateGaps does not error when burnDownSnapshots is an empty array", () => {
  const burnDownSnapshots = [];
  const result = fillInSnapshotDateGaps({ burnDownSnapshots });
  expect(result).toEqual([]);
});

test("addEventColorsToLogEntries adds colors to activity log entries", () => {
  const eventTypes = {
    1: {
      id: 1,
      name: "CARD_STARTED",
      description: null,
    },
    2: {
      id: 2,
      name: "CARD_REVIEW_REQUESTED",
      description: null,
    },
    3: {
      id: 3,
      name: "CARD_REVIEW_REQUEST_CANCELLED",
      description: null,
    },
    4: {
      id: 4,
      name: "COMPETENCE_REVIEW_DONE",
      description: null,
    },
    5: {
      id: 5,
      name: "CARD_MOVED_TO_COMPLETE",
      description: null,
    },
    6: {
      id: 6,
      name: "CARD_MOVED_TO_REVIEW_FEEDBACK",
      description: null,
    },
  };
  const activityLogEntries = [
    {
      id: 129,
      timestamp: "2022-10-06T09:07:03.401226Z",
      eventType: 2,
      actorUser: 18,
      effectedUser: 18,
      actorUserEmail: "faith.mofokeng@umuzi.org",
      effectedUserEmail: "faith.mofokeng@umuzi.org",
      object1ContentTypeName: "curriculum_tracking | topic progress",
      object1Id: 16,
      object2ContentTypeName: null,
      object2Id: null,
      object1Summary: {
        topicProgress: 16,
        card: 76,
        title: "Understanding the review column",
        flavourNames: [],
      },
      object2Summary: null,
    },
  ];
  const newData = [
    {
      id: 129,
      timestamp: "2022-10-06T09:07:03.401226Z",
      eventType: 2,
      actorUser: 18,
      effectedUser: 18,
      actorUserEmail: "faith.mofokeng@umuzi.org",
      effectedUserEmail: "faith.mofokeng@umuzi.org",
      object1ContentTypeName: "curriculum_tracking | topic progress",
      object1Id: 16,
      object2ContentTypeName: null,
      object2Id: null,
      object1Summary: {
        topicProgress: 16,
        card: 76,
        title: "Understanding the review column",
        flavourNames: [],
      },
      object2Summary: null,
      eventName: "CARD_REVIEW_REQUESTED",
      eventColor: "#fb8c00",
    },
  ];
  expect(
    addEventColorsToLogEntries({
      eventTypes,
      activityLogEntries,
    })
  ).toEqual(newData);
});
