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
  IoHammerOutline,
  IoBookOutline,
} from "react-icons/io5";
// https://react-icons.github.io/react-icons/icons?name=io5

export const statusLooks = {
  [STATUS_DONE]: {
    Icon: IoCheckmarkOutline,
    color: "green",
  },
  [STATUS_READY]: {
    Icon: IoPlayOutline,
    color: "blue",
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
  [COMPETENT]: {
    Icon: IoCheckmarkCircleOutline,
    color: statusLooks[STATUS_DONE].color,
    title: "You passed",
  },
  [NOT_YET_COMPETENT]: {
    Icon: IoCloseCircleOutline,
    color: statusLooks[STATUS_ERROR].color,
    title: "Not yet competent, please try again",
  },
};

export const BackArrowIcon = IoArrowBackOutline;
export const ForwardArrowIcon = IoArrowForwardOutline;

export const ProjectIcon = IoHammerOutline;
export const ContentIcon = IoBookOutline;
