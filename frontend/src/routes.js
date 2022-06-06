// import UserProfile from "./components/regions/UserProfile";
import AgileBoard from "./components/regions/AgileBoard";
import UserActions from "./components/regions/UserActions";
import UsersAndGroups from "./components/pages/UsersAndGroups";
import GroupCardSummary from "./components/pages/GroupCardSummary";
import CardDetails from "./components/pages/CardDetails";
import Redirector from "./components/regions/Redirector";
import TeamDashboard from "./components/pages/TeamDashboard";
import UserDashboard from "./components/pages/UserDashboard";

import { TEAM_PERMISSIONS } from "./constants";

import UserNavBar from "./components/regions/UserNavBar";
import TeamNavBar from "./components/regions/TeamNavBar";
import ForgotPassword from "./components/pages/ForgotPassword";
import ForgotPasswordConfirm from "./components/pages/ForgotPasswordConfirm";
import LoginForm from "./components/pages/Login";

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
      path: "/forgot_password_confirm",
    },
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
      //     //these get used to draw buttons in the left hand side slider/hamburger menu
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

  userNavBar: {
    route: {
      exact: false,
      path: "/users/:userId/",
    },
    component: UserNavBar,
  },

  userBoard: {
    route: {
      exact,
      path: "/users/:userId/board",
    },
    component: AgileBoard,
  },

  userActions: {
    route: {
      exact,
      path: "/users/:userId/actions",
    },
    component: UserActions,
  },

  teamNavBar: {
    route: {
      exact: false,
      path: "/teams/:teamId/",
    },
    component: TeamNavBar,
  },

  groupCardSummary: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/card_summary",
    },
    component: GroupCardSummary,
    show: () => true,
  },

  teamDashboard: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/dashboard",
    },
    component: TeamDashboard,
    show: () => true,
  },

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
