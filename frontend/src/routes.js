// import TimelineIcon from "@material-ui/icons/Timeline";
// // import LocalLibraryIcon from "@material-ui/icons/LocalLibrary";
// import RoomIcon from "@material-ui/icons/Room";
// import StarIcon from "@material-ui/icons/Star";

import UserProfile from "./components/regions/UserProfile";
import Dashboard from "./components/regions/Dashboard";
import RecruitAgileBoard from "./components/regions/RecruitAgileBoard";
// import Library from "./components/regions/Library";
// import Favourites from "./components/regions/Favourites";

const exact = true;

export const routes = {
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
