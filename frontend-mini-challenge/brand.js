import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_READY,
  STATUS_UNDER_REVIEW,
  STATUS_ERROR,
  COMPETENT,
  NOT_YET_COMPETENT,
} from "./constants";

import {
  IoPlayOutline,
  IoCheckmarkOutline,
  IoCheckmarkCircleOutline,
  IoLockClosedOutline,
  IoAlertCircleOutline,
  IoPersonCircleOutline,
  IoSettingsOutline,
  IoLogOutOutline,
  IoInformationCircleOutline,
  IoSyncOutline,
  IoArrowBackOutline,
  IoArrowForwardOutline,
  IoCloseCircleOutline,
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
  [STATUS_UNDER_REVIEW]: {
    Icon: IoSyncOutline,
    color: "orange",
  },
  [STATUS_ERROR]: {
    Icon: IoAlertCircleOutline,
    color: "red",
  },
};

export const ErrorIcon = IoAlertCircleOutline;
export const InfoIcon = IoInformationCircleOutline;

export const ProfileIcon = IoPersonCircleOutline;
export const SettingsIcon = IoSettingsOutline;
export const LogoutIcon = IoLogOutOutline;

export const ReviewStatusLooks = {
  COMPETENT: {
    Icon: IoCheckmarkCircleOutline,
  },
  NOT_YET_COMPETENT: {
    Icon: IoCloseCircleOutline,
  },
};

export const BackArrowIcon = IoArrowBackOutline;
export const ForwardArrowIcon = IoArrowForwardOutline;
