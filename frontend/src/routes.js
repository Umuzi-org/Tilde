// import UserProfile from "./components/regions/UserProfile";
import AgileBoard from "./components/pages/AgileBoard";
import UserActions from "./components/pages/UserActions";
import UsersAndGroups from "./components/pages/UsersAndGroups";
import GroupCardSummary from "./components/pages/GroupCardSummary";
import CardDetails from "./components/pages/CardDetails";
import Redirector from "./components/regions/Redirector";
// import TeamDashboard from "./components/pages/TeamDashboard";
import UserDashboard from "./components/pages/UserDashboard";
import GlobalCodeReviewDashboard from "./components/pages/GlobalCodeReviewDashboard";
import { TEAM_PERMISSIONS } from "./constants";

import UserNavBar from "./components/regions/UserNavBar";
import TeamNavBar from "./components/regions/TeamNavBar";
import ForgotPassword from "./components/pages/ForgotPassword";
import ForgotPasswordConfirm from "./components/pages/ForgotPasswordConfirm";
import LoginForm from "./components/pages/Login";
import UserCodeReviewPerformance from "./components/pages/UserCodeReviewPerformance";

const exact = true;

export const routes = {
  login: {
    route: {
      exact,
      path: "/login",
    },
    component: LoginForm,
    anonymousRoute: true, // only available if the user is not logged in
  },

  forgotPassword: {
    route: {
      exact,
      path: "/forgot_password",
    },
    component: ForgotPassword,
    anonymousRoute: true, // only available if the user is not logged in
  },

  forgotPasswordConfirm: {
    route: {
      exact,
      path: "/password-reset-confirm/:uid/:token",
    },
    matchPattern: "/password-reset-confirm/",
    component: ForgotPasswordConfirm,
    anonymousRoute: true,
  },

  homeRedirect: {
    route: {
      exact,
      path: "/",
    },
    component: Redirector, // todo: fix spelling
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "B",
      label: "Your Board",
      helpText: "Your board",
    },
    show: () => true,
  },

  groupNav: {
    route: {
      // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
      exact,
      path: "/users",
    },
    component: UsersAndGroups,
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "U",
      label: "Users",
      helpText: "User and Team navigation",
    },
    show: ({ authUser }) => {
      if (authUser.isSuperuser) return true;

      for (let teamId in authUser.permissions.teams) {
        for (let permission of authUser.permissions.teams[teamId].permissions) {
          if (TEAM_PERMISSIONS.includes(permission)) return true;
          throw new Error(`Team permission not implemented: ${permission}`);
        }
      }
    },
    userMustBeLoggedIn: true,
  },

  globalCodeReviewDashboard: {
    route: {
      exact,
      path: "/code_review_dashboard",
    },
    component: GlobalCodeReviewDashboard,
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "R",
      label: "Code Review Dash",
      helpText: "Code review dashboard",
    },
    show: ({ authUser }) => {
      if (authUser.isSuperuser) return true;

      for (let teamId in authUser.permissions.teams) {
        for (let permission of authUser.permissions.teams[teamId].permissions) {
          if (TEAM_PERMISSIONS.includes(permission)) return true;
          throw new Error(`Team permission not implemented: ${permission}`);
        }
      }
    },
    userMustBeLoggedIn: true,
  },

  userBoard: {
    route: {
      exact,
      path: "/users/:userId/board",
    },
    component: AgileBoard,
    navBarComponent: UserNavBar,
  },

  userActions: {
    route: {
      exact,
      path: "/users/:userId/actions",
    },
    component: UserActions,
    navBarComponent: UserNavBar,
  },

  groupCardSummary: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/card_summary",
    },
    component: GroupCardSummary,
    navBarComponent: TeamNavBar,

    show: () => true,
  },

  // teamDashboard: {
  //   // todo Rename this to teamCardSummary
  //   route: {
  //     exact,
  //     path: "/teams/:teamId/dashboard",
  //   },
  //   component: TeamDashboard,
  //   navBarComponent: TeamNavBar,
  //   show: () => true,
  // },

  // profile: {
  //   // TODO: What is in this component? Can we just delete it?
  //   route: {
  //     exact,
  //     path: "/people/:id",
  //   },
  //   component: UserProfile,
  // },

  userDashboard: {
    route: {
      exact,
      path: "/users/:userId/dashboard",
    },
    component: UserDashboard,
    navBarComponent: UserNavBar,
  },

  userCodeReviewPerformance: {
    route: {
      exact,
      path: "/users/:userId/review_performance",
    },
    component: UserCodeReviewPerformance,
    navBarComponent: UserNavBar,
  },

  cardDetails: {
    route: {
      exact,
      path: "/card/:cardId",
    },
    component: CardDetails,

    show: () => true,
  },
};
