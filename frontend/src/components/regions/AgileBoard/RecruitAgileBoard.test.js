// import React from "react";
// import { render } from "@testing-library/react";
// import App from ".";

// test("renders learn react link", () => {
//   render(<App />);
//   //   const { getByText } = render(<App />);
//   //   const linkElement = getByText(/learn react/i);
//   //   expect(linkElement).toBeInTheDocument();
// });

import { getLatestCallNextPageValue } from ".";

const fetchCardsCallLog = [
  {
    loading: false,
    requestData: { page: 1, assigneeUserId: 8, status: "B" },
    error: null,
    responseData: {
      count: 10,
      next: null,
      previous: null,
      results: [
        {
          id: 10022,
          contentItem: 1633,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Assertive programming kata",
          contentType: "project",
          storyPoints: 1,
          tagNames: [],
          order: 25,
        },
        {
          id: 10024,
          contentItem: 1493,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Data Ethics",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: ["data-ethics"],
          order: 28,
        },
        {
          id: 10026,
          contentItem: 1627,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Test Driven Development",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["tdd"],
          order: 30,
        },
        {
          id: 10027,
          contentItem: 1694,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Evolution of Linux Visualisation",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["data-visualisation-datacamp"],
          order: 33,
        },
        {
          id: 10031,
          contentItem: 1696,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Data Wrangling",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["data-wrangling"],
          order: 39,
        },
        {
          id: 10034,
          contentItem: 1681,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "OOP for data science",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["oop-data-sci"],
          order: 45,
        },
        {
          id: 10036,
          contentItem: 1507,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Environmental Variables",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 48,
        },
        {
          id: 10037,
          contentItem: 1517,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Intro to Docker and Docker-compose",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["docker-compose", "postgres"],
          order: 49,
        },
        {
          id: 10038,
          contentItem: 1649,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "SQL",
          contentType: "project",
          storyPoints: 1,
          tagNames: [],
          order: 50,
        },
        {
          id: 10047,
          contentItem: 1686,
          status: "B",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Natural language processing",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["nlp"],
          order: 61,
        },
      ],
    },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, assigneeUserId: 8, status: "R" },
    error: null,
    responseData: {
      count: 38,
      next: "http://127.0.0.1:8000/api/agile_card/?assignees=8&page=2&status=R",
      previous: null,
      results: [
        {
          id: 10000,
          contentItem: 1624,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Agile & Scrum",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 0,
        },
        {
          id: 10001,
          contentItem: 1492,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Agile and Scrum",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 1,
        },
        {
          id: 10002,
          contentItem: 1461,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "How to be a professional",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 2,
        },
        {
          id: 10003,
          contentItem: 1508,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Introduction to Linux",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["linux"],
          order: 3,
        },
        {
          id: 10004,
          contentItem: 1510,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Introduction to Bash and the terminal",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["bash"],
          order: 4,
        },
        {
          id: 10005,
          contentItem: 1467,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Introduction to Linux: Live demo",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: ["todo"],
          order: 5,
        },
        {
          id: 10006,
          contentItem: 1502,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Python self-learning",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 7,
        },
        {
          id: 10007,
          contentItem: 1535,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Clean Code for Python",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 8,
        },
        {
          id: 10008,
          contentItem: 1592,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Git Basics",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["todo"],
          order: 9,
        },
        {
          id: 10009,
          contentItem: 1668,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Level 1 programming katas",
          contentType: "project",
          storyPoints: 1,
          tagNames: [],
          order: 11,
        },
        {
          id: 10010,
          contentItem: 1490,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "What to Put On A CV",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 12,
        },
        {
          id: 10011,
          contentItem: 1523,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Introduction to web design",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 13,
        },
        {
          id: 10012,
          contentItem: 1457,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Intro to CSS architecture",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 14,
        },
        {
          id: 10013,
          contentItem: 1577,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "How to ask for help with your code",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 16,
        },
        {
          id: 10014,
          contentItem: 1469,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Clean Code (language agnostic)",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 17,
        },
        {
          id: 10015,
          contentItem: 1487,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Basic Intro to OOP",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: ["todo"],
          order: 18,
        },
        {
          id: 10016,
          contentItem: 1617,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Python OOP basics",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["todo", "oop"],
          order: 19,
        },
        {
          id: 10017,
          contentItem: 1613,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Automated Testing in Python",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 20,
        },
        {
          id: 10018,
          contentItem: 1614,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Virtual Environments",
          contentType: "topic",
          storyPoints: 1,
          tagNames: ["todo"],
          order: 21,
        },
        {
          id: 10019,
          contentItem: 1483,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Survey design",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 22,
        },
        {
          id: 10020,
          contentItem: 1491,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Google forms like a boss",
          contentType: "workshop",
          storyPoints: 1,
          tagNames: [],
          order: 23,
        },
        {
          id: 10021,
          contentItem: 1594,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Introduction to assertive programming",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 24,
        },
        {
          id: 10025,
          contentItem: 1504,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Unit testing (language agnostic concepts)",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 29,
        },
        {
          id: 10028,
          contentItem: 1501,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Jupyter notebooks best practices",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 34,
        },
        {
          id: 10029,
          contentItem: 1632,
          status: "R",
          recruitProject: null,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "The Tech Landscape Terminology",
          contentType: "topic",
          storyPoints: 1,
          tagNames: [],
          order: 37,
        },
      ],
    },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, assigneeUserId: 8, status: "IP" },
    error: null,
    responseData: {
      count: 17,
      next: null,
      previous: null,
      results: [
        {
          id: 8322,
          contentItem: 1702,
          status: "IP",
          recruitProject: 3330,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Predict breast cancer",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["logistic-regression"],
          order: 0,
        },
        {
          id: 8349,
          contentItem: 1701,
          status: "IP",
          recruitProject: 3345,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Predict credit card approvals",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["datacamp-logistic-regression"],
          order: 0,
        },
        {
          id: 8750,
          contentItem: 1678,
          status: "IP",
          recruitProject: 3741,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Bank Accounts",
          contentType: "project",
          storyPoints: 1,
          tagNames: [],
          order: 0,
        },
        {
          id: 9258,
          contentItem: 1704,
          status: "IP",
          recruitProject: 4269,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Getting to know Python",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["todo"],
          order: 0,
        },
        {
          id: 9525,
          contentItem: 1637,
          status: "IP",
          recruitProject: 4535,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Beginner Linux challenges",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["todo", "bash"],
          order: 6,
        },
        {
          id: 9535,
          contentItem: 1737,
          status: "IP",
          recruitProject: 4558,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Git Basic Exercises",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["git"],
          order: 10,
        },
        {
          id: 9413,
          contentItem: 1669,
          status: "IP",
          recruitProject: 4498,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Build your first personal website",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["html", "css"],
          order: 15,
        },
        {
          id: 9371,
          contentItem: 1695,
          status: "IP",
          recruitProject: 4379,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Data Visualisation Projects",
          contentType: "project",
          storyPoints: 1,
          tagNames: [],
          order: 26,
        },
        {
          id: 9484,
          contentItem: 1722,
          status: "IP",
          recruitProject: 4485,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "simple-calculator part 1",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["tdd"],
          order: 31,
        },
        {
          id: 9257,
          contentItem: 1715,
          status: "IP",
          recruitProject: 4268,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "string-calculator",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["tdd", "regular-expressions"],
          order: 32,
        },
        {
          id: 9171,
          contentItem: 1693,
          status: "IP",
          recruitProject: 4146,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: false,
          isSoftMilestone: false,
          title: "Financial Services Use in Tanzania",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["data-visualisation-mobile-money"],
          order: 35,
        },
        {
          id: 9138,
          contentItem: 1697,
          status: "IP",
          recruitProject: 4143,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Statistical Thinking",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["stats"],
          order: 36,
        },
        {
          id: 8867,
          contentItem: 1683,
          status: "IP",
          recruitProject: 3868,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Cross-validation & Simple Linear Regression",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["simple-linear-regression"],
          order: 40,
        },
        {
          id: 8625,
          contentItem: 1682,
          status: "IP",
          recruitProject: 3641,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Multivariate Linear Regression",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["multiple-linear-regression"],
          order: 41,
        },
        {
          id: 8484,
          contentItem: 1689,
          status: "IP",
          recruitProject: 3482,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Plotly Dashboard Assignment",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["plotly"],
          order: 46,
        },
        {
          id: 8231,
          contentItem: 1685,
          status: "IP",
          recruitProject: 3243,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "Decision Trees",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["decision-trees"],
          order: 53,
        },
        {
          id: 9759,
          contentItem: 1684,
          status: "IP",
          recruitProject: 4790,
          assignees: [8],
          reviewers: [],
          assigneeNames: ["masai.mahapa@umuzi.org"],
          reviewerNames: [],
          isHardMilestone: true,
          isSoftMilestone: false,
          title: "K-Means Clustering Assignment",
          contentType: "project",
          storyPoints: 1,
          tagNames: ["kmeans"],
          order: 59,
        },
      ],
    },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, assigneeUserId: 8, status: "RF" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, assigneeUserId: 8, status: "IR" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, assigneeUserId: 8, status: "C" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, reviewerUserId: 8, status: "B" },
    error: null,
    responseData: {
      count: 0,
      next: "http://127.0.0.1:8000/api/agile_card/?assignees=8&page=3&status=R",
      previous: null,
      results: [],
    },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, reviewerUserId: 8, status: "R" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, reviewerUserId: 8, status: "IP" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, reviewerUserId: 8, status: "RF" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, reviewerUserId: 8, status: "IR" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
  {
    loading: false,
    requestData: { page: 1, reviewerUserId: 8, status: "C" },
    error: null,
    responseData: { count: 0, next: null, previous: null, results: [] },
    responseOk: true,
    successLog: [],
  },
];

test("getLatestCallNextPageValue", () => {
  let page;

  page = getLatestCallNextPageValue({ fetchCardsCallLog, status: "fake" });
  expect(page).toBe(null);

  page = getLatestCallNextPageValue({
    fetchCardsCallLog,
    status: "B",
    assigneeUserId: 8,
  });
  expect(page).toBe(null);

  page = getLatestCallNextPageValue({
    fetchCardsCallLog,
    status: "R",
    assigneeUserId: 8,
  });
  expect(page).toBe(2);

  page = getLatestCallNextPageValue({
    fetchCardsCallLog,
    status: "B",
    reviewerUserId: 8,
  });
  expect(page).toBe(3);

  page = getLatestCallNextPageValue({
    fetchCardsCallLog,
    status: "R",
    reviewerUserId: 8,
  });
  expect(page).toBe(null);
});
