import { STATUS_BLOCKED, STATUS_DONE, STATUS_READY } from "./data";

import {
  IoPlayOutline,
  IoCheckmarkOutline,
  IoLockClosedOutline,
} from "react-icons/io5";

export const statusLooks = {
  [STATUS_DONE]: {
    Icon: IoCheckmarkOutline,
    color: "blue",
  },
  [STATUS_READY]: {
    Icon: IoPlayOutline,
    color: "green",
  },
  [STATUS_BLOCKED]: {
    Icon: IoLockClosedOutline,
    color: "grey",
  },

  // IoSyncOutline
};
