import UserProfile from "./components/regions/UserProfile";
import AgileBoard from "./components/regions/AgileBoard";
import GroupCardSummary from "./components/regions/GroupCardSummary";
import UsersAndGroups from "./components/regions/UsersAndGroups";

import { TEAM_PERMISSIONS } from "./constants";

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
    },
    show: () => true,
  },

  userBoard: {
    route: {
      exact,
      path: "/boards/:userId",
      component: AgileBoard,
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
};
