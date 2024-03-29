# Statuses for different project configs

CONFIG_STATUS_DEBUG = "DEBUG"
CONFIG_STATUS_PRODUCTION = "PRODUCTION"
CONFIG_STATUS_DEACTIVATED = "DEACTIVATED"
CONFIG_STATUS_NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

CONFIG_ALLOWED_STATUSES = [
    CONFIG_STATUS_DEBUG,
    CONFIG_STATUS_PRODUCTION,
    CONFIG_STATUS_DEACTIVATED,
    CONFIG_STATUS_NOT_IMPLEMENTED,
]


STEP_STATUS_PASS = "pass"  # finished without error
STEP_STATUS_NOT_YET_COMPETENT = "not yet competent"
STEP_STATUS_RED_FLAG = "red flag"
STEP_STATUS_WAITING = "waiting"
STEP_STATUS_RUNNING = "running"
STEP_STATUS_ERROR = "error"  # something unexpected broke

STEP_FINAL_STATUSES = [
    # NOTE: the ordering here matters. Eg if all steps pass and there is one red flag then the red flag takes precedence. The overall run is a red flag.
    STEP_STATUS_WAITING,  # a step can end in this status if a previous step failed]
    STEP_STATUS_PASS,
    STEP_STATUS_ERROR,
    STEP_STATUS_NOT_YET_COMPETENT,
    STEP_STATUS_RED_FLAG,
]
