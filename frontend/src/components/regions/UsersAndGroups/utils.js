const PR_WARNING_AGE_THRESHOLD = 1
const PR_ERROR_AGE_THRESHOLD = 2
const TILDE_ERROR_AGE_THRESHOLD = 3
const TILDE_WARNING_AGE_THRESHOLD = 2

const ERROR_STATUS = "error"
const WARNING_STATUS = "warning"
const DEFAULT_STATUS = "default"

export const timeDifferenceInDays = (time) => {
  return Math.ceil(Math.abs(new Date() - new Date(time)) / (1000 * 3600 * 24) - 1)
}

export const getPrStatus = (oldestOpenPrTime) => {
  const ageInDays = timeDifferenceInDays(oldestOpenPrTime)
  if (ageInDays >= PR_ERROR_AGE_THRESHOLD){
    return ERROR_STATUS;
  }
  if(ageInDays >= PR_WARNING_AGE_THRESHOLD){
    return WARNING_STATUS
  }
  return DEFAULT_STATUS
};

export const getTildeReviewStatus = (oldestOpenTildeReviewTime) => {
  const ageInDays = timeDifferenceInDays(oldestOpenTildeReviewTime)
  if (ageInDays >= TILDE_ERROR_AGE_THRESHOLD){
    return ERROR_STATUS;
  }
  if(ageInDays >= TILDE_WARNING_AGE_THRESHOLD){
    return WARNING_STATUS
  }
  return DEFAULT_STATUS
  
};
