import { updateBurnDownSnapshots, removeDuplicateDates } from "./utils";
test("updateBurnDownSnapshots returns updated burnDownSnapshots with gap dates filled", () => {
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
  const result = updateBurnDownSnapshots({ burnDownSnapshots });
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