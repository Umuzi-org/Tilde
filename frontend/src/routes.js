import UserProfile from "./components/regions/UserProfile";
import Dashboard from "./components/regions/Dashboard";
import RecruitAgileBoard from "./components/regions/RecruitAgileBoard";
import UsersAndGroups from "./components/regions/UsersAndGroups";

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
    show: ({ authUser }) => authUser.isStaff,
  },

  board: {
    route: {
      // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
      exact,
      path: "/",
      component: RecruitAgileBoard,
    },
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      icon: () => "B",
      label: "Board",
    },
    show: () => true,
  },

  dashboard: {
    route: {
      // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
      exact,
      path: "/summary",
      component: Dashboard,
    },
    sliderNavigation: {
      //these get used to draw buttons in the left hand side slider/hamburger menu
      //   icon: TimelineIcon,
      icon: () => "P",

      label: "Projects",
    },
    show: ({ authUser }) => authUser.isStaff,
  },
  userBoard: {
    route: {
      exact,
      path: "/boards/:id",
      component: RecruitAgileBoard,
    },
  },

  //   library: {
  //     route: {
  //       // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
  //       exact,
  //       path: "/library",
  //       component: Library,
  //     },
  //     sliderNavigation: {
  //       //these get used to draw buttons in the left hand side slider/hamburger menu
  //       icon: LocalLibraryIcon,
  //       label: "Library",
  //     },
  //   },

  //   favourites: {
  //     route: {
  //       // these are the arguments for the "Route" component. Eg: <Route exact path="/" component={Home}/>
  //       exact,
  //       path: "/favourites",
  //       component: Favourites,
  //     },
  //     sliderNavigation: {
  //       //these get used to draw buttons in the left hand side slider/hamburger menu
  //       icon: StarIcon,
  //       label: "Favourites",
  //     },
  //   },

  profile: {
    route: {
      exact,
      path: "/people/:id",
      component: UserProfile,
    },
  },
};
