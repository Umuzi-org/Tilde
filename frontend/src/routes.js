import UserProfile from "./components/regions/UserProfile";
import AgileBoard from "./components/regions/AgileBoard";
import UserActions from "./components/regions/UserActions";
import GroupCardSummary from "./components/regions/GroupCardSummary";
import UsersAndGroups from "./components/regions/UsersAndGroups";
import Dashboard from "./components/regions/Dashboard";
import CardDetails from "./components/regions/CardDetails";

import { TEAM_PERMISSIONS } from "./constants";

import UserNavBar from "./components/regions/UserNavBar";
const exact = true;

export const routes = {
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
  },

  board: {
    route: {
      // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
      exact,
      path: "/",
      component: AgileBoard,
    },
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "B",
      label: "Board",
      helpText: "Your personal board",
    },
    show: () => true,
  },

  actions: {
    route: {
      // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
      exact,
      path: "/actions",
      component: UserActions,
    },
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "A",
      label: "Actions",
      helpText: "Your personal action log",
    },
    show: () => true,
  },

  userNavBar: {
    route: {
      exact: false,
      path: "/users/:userId/",
      component: UserNavBar,
    },
  },

  userBoard: {
    route: {
      exact,
      path: "/users/:userId/board",
      component: AgileBoard,
    },
  },

  userActions: {
    route: {
      exact,
      path: "/users/:userId/actions",
      component: UserActions,
    },
  },

  groupCardSummary: {
    route: {
      exact,
      path: "/teams/:teamId/card_summary",
      component: GroupCardSummary,
    },
    show: () => true,
  },

  profile: {
    route: {
      exact,
      path: "/people/:id",
      component: UserProfile,
    },
  },

  userDashboard: {
    route: {
      exact,
      path: "/users/:userId/dashboard",
      component: Dashboard,
    },
  },

  dashboard: {
    route: {
      exact,
      path: "/dashboard",
      component: Dashboard,
    },

    show: () => true,
  },

  cardDetails: {
    route: {
      exact,
      path: "/card/:cardId",
      component: CardDetails,
    },

    show: () => true,
  },
};
