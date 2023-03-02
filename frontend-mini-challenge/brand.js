import { STATUS_BLOCKED, STATUS_DONE, STATUS_READY } from "./data";

import {
  IoPlayOutline,
  IoCheckmarkOutline,
  IoLockClosedOutline,
  IoAlertCircleOutline,
  IoPersonCircleOutline,
  IoSettingsOutline,
  IoLogOutOutline,
  IoInformationCircleOutline,
} from "react-icons/io5";
// https://react-icons.github.io/react-icons/icons?name=io5

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
};

export const ErrorIcon = IoAlertCircleOutline;
export const InfoIcon = IoInformationCircleOutline;

export const ProfileIcon = IoPersonCircleOutline;
export const SettingsIcon = IoSettingsOutline;
export const LogoutIcon = IoLogOutOutline;
