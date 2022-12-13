import React from "react";
import GlobalCodeReviewDashboard from "../components/pages/GlobalCodeReviewDashboard/Presentation";
import { BrowserRouter as Router } from "react-router-dom";
import competenceReviewProjects from "./fixtures/GlobalCodeReviewDashboard/competenceReviewQueueProjects.json";
import pullRequestReviewProjects from "./fixtures/GlobalCodeReviewDashboard/pullRequestReviewQueueProjects.json";

export default {
  title: "Tilde/pages/GlobalCodeReviewDashboard",
  component: GlobalCodeReviewDashboard,
};

const Template = (args) => (
  <Router>
    <GlobalCodeReviewDashboard {...args} />
  </Router>
);

export const Primary = Template.bind({});

const initialPullRequestOrderFilters = [
  {
    label: "last updated time",
    sortInAscendingOrder: () => {},
    sortInDescendingOrder: () => {},
    isSelected: true,
    isAscending: false,
  },
];
const initialCompetenceOrderFilters = [
  {
    label: "review request time",
    sortInAscendingOrder: () => {},
    sortInDescendingOrder: () => {},
    isSelected: true,
    isAscending: false,
  },
  {
    label: "start time",
    sortInAscendingOrder: () => {},
    sortInDescendingOrder: () => {},
    isSelected: false,
    isAscending: false,
  },
  {
    label: "positive reviews",
    sortInAscendingOrder: () => {},
    sortInDescendingOrder: () => {},
    isSelected: false,
    isAscending: false,
  },
];
const selectedCompetenceOrderFilter = initialCompetenceOrderFilters[0];
const selectedPullRequestOrderFilter = initialCompetenceOrderFilters[0];

Primary.args = {
  competenceReviewQueueProjects: competenceReviewProjects,
  pullRequestReviewQueueProjects: pullRequestReviewProjects,
  competenceReviewQueueLoading: false,
  pullRequestReviewQueueLoading: false,
  filterIncludeTags: ["clustering"],
  filterExcludeTags: ["data structures"],
  filterIncludeFlavours: ["python"],
  filterExcludeFlavours: ["python"],
  allFlavours: ["javascript", "python", "react", "java", "django"],
  allTagNames: ["ncit", "decision-trees", "todo", "ncit", "internet"],
  allTeamNames: ["A", "B", "C"],
  filterIncludeAssigneeTeams: ["B"],
  competenceOrderFilters: initialCompetenceOrderFilters,
  pullRequestOrderFilters: initialPullRequestOrderFilters,
  selectedCompetenceOrderFilter: selectedCompetenceOrderFilter,
  selectedPullRequestOrderFilter: selectedPullRequestOrderFilter,
  applyFilters: () => true,
  setPullRequestOrderFilters: () => {},
  fetchNextCompetenceReviewQueuePage: () => {},
  fetchNextPullRequestQueuePage: () => {},
  setCompetenceOrderFilters: () => {},
  setSelectedCompetenceOrderFilter: () => {},
  handleChangeFlavourFilter: () => {},
  handleChangeTagFilter: () => {},
  handleChangeAssigneeTeamFilter: () => {},
};
