import UserProfile from "./components/regions/UserProfile";
import AgileBoard from "./components/regions/AgileBoard";
import UserActions from "./components/regions/UserActions";
import GroupCardSummary from "./components/regions/GroupCardSummary";
import UsersAndGroups from "./components/regions/UsersAndGroups";
import UserDashboard from "./components/regions/UserDashboard";
import CardDetails from "./components/regions/CardDetails";
import Redirector from "./components/regions/Redirector";
import TeamDashboard from "./components/pages/TeamDashboard";
import LoginForm from "./components/regions/Login";
import ForgotPassword from "./components/regions/Login/ForgotPassword";

import { TEAM_PERMISSIONS } from "./constants";

import UserNavBar from "./components/regions/UserNavBar";
import TeamNavBar from "./components/regions/TeamNavBar";

const exact = true;

export const routes = {
  login: {
    route: {
      exact,
      path: "/login",
      component: LoginForm,
    },
    userMustBeLoggedIn: false,
  },

  forgotPassword: {
    route: {
      exact,
      path: "/forgotPassword",
      component: ForgotPassword,
    },
    userMustBeLoggedIn: false,
  },

  homeRedirect: {
    route: {
      exact,
      path: "/",
      component: Redirector, // todo: fix spelling
    },
    sliderNavigation: {
      //     //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "B",
      label: "Your Board",
      helpText: "Your board",
    },
    show: () => true,
    userMustBeLoggedIn: true,
  },

  groupNav: {
    route: {
      // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
      exact,
      path: "/users",
      component: UsersAndGroups,
    },
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
      component: UserNavBar,
    },
    userMustBeLoggedIn: true,
  },

  userBoard: {
    route: {
      exact,
      path: "/users/:userId/board",
      component: AgileBoard,
    },
    userMustBeLoggedIn: true,
  },

  userActions: {
    route: {
      exact,
      path: "/users/:userId/actions",
      component: UserActions,
    },
    userMustBeLoggedIn: true,
  },

  teamNavBar: {
    route: {
      exact: false,
      path: "/teams/:teamId/",
      component: TeamNavBar,
    },
    userMustBeLoggedIn: true,
  },

  groupCardSummary: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/card_summary",
      component: GroupCardSummary,
    },
    show: () => true,
    userMustBeLoggedIn: true,
  },

  teamDashboard: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/dashboard",
      component: TeamDashboard,
    },
    show: () => true,
    userMustBeLoggedIn: true,
  },

  profile: {
    // TODO: What is in this component? Can we just delete it?
    route: {
      exact,
      path: "/people/:id",
      component: UserProfile,
    },
    userMustBeLoggedIn: true,
  },

  userDashboard: {
    route: {
      exact,
      path: "/users/:userId/dashboard",
      component: UserDashboard,
    },
    userMustBeLoggedIn: true,
  },

  cardDetails: {
    route: {
      exact,
      path: "/card/:cardId",
      component: CardDetails,
    },

    show: () => true,
    userMustBeLoggedIn: true,
  },
};
