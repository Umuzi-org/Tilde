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
const exact = true;

export const routes = {
  homeRedirect: {
    route: {
      exact,
      path: "/",
    },
    Component: Redirector, // todo: fix spelling
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
    Component: UsersAndGroups,
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

  userBoard: {
    route: {
      exact,
      path: "/users/:userId/board",
    },
    Component: AgileBoard,
    NavBarComponent: UserNavBar,
  },

  userActions: {
    route: {
      exact,
      path: "/users/:userId/actions",
    },
    Component: UserActions,
    NavBarComponent: UserNavBar,
  },

  // teamNavBar: {
  //   route: {
  //     exact: false,
  //     path: "/teams/:teamId/",
  //   },
  //   Component: TeamNavBar,
  // },

  groupCardSummary: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/card_summary",
    },
    Component: GroupCardSummary,
    NavBarComponent: TeamNavBar,
    show: () => true,
  },

  teamDashboard: {
    // todo Rename this to teamCardSummary
    route: {
      exact,
      path: "/teams/:teamId/dashboard",
    },
    Component: TeamDashboard,
    NavBarComponent: TeamNavBar,

    show: () => true,
  },

  // profile: {
  //   // TODO: What is in this component? Can we just delete it?
  //   route: {
  //     exact,
  //     path: "/people/:id",
  //   },
  //   Component: UserProfile,
  // },

  userDashboard: {
    route: {
      exact,
      path: "/users/:userId/dashboard",
    },
    Component: UserDashboard,
    NavBarComponent: UserNavBar,
  },

  cardDetails: {
    route: {
      exact,
      path: "/card/:cardId",
    },
    Component: CardDetails,

    show: () => true,
  },
};
