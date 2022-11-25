import { fillInSnapshotDateGaps } from "./utils";
test("fillInSnapshotDateGaps returns updated currentUserBurndownStats with gap dates filled", () => {
  const currentUserBurndownStats = [
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
  const result = fillInSnapshotDateGaps({ currentUserBurndownStats });
  expect(result).toEqual(sampleUpdatedBurnDownSnapshots);
});

test("fillInSnapshotDateGaps does not error when burnDownSnapshots is an empty array", () => {
  const currentUserBurndownStats = [];
  const result = fillInSnapshotDateGaps({ currentUserBurndownStats });
  expect(result).toEqual([]);
});
