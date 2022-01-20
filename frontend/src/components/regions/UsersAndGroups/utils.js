const PR_WARNING_AGE_THRESHOLD = 1
const PR_ERROR_AGE_THRESHOLD = 2
const TILDE_ERROR_AGE_THRESHOLD = 3
const TILDE_WARNING_AGE_THRESHOLD = [1,2]
export const timeDifferenceInDays = (time) => {
  return Math.ceil(Math.abs(new Date() - new Date(time)) / (1000 * 60 * 60 * 24) - 1)
}

export const getPrStatus = (oldestOpenPrTime) => {
  const ageInDays = timeDifferenceInDays(oldestOpenPrTime)
  if (ageInDays >= PR_ERROR_AGE_THRESHOLD){
    return "error";
  }
  if(ageInDays === PR_WARNING_AGE_THRESHOLD){
    return "warning"
  }
  return "default"
};

export const getTildeReviewStatus = (oldestOPenTildeReviewTime) => {
  const ageInDays = timeDifferenceInDays(oldestOPenTildeReviewTime)
  console.log(ageInDays)
  if (ageInDays >= TILDE_ERROR_AGE_THRESHOLD){
    return "error";
  }
  if((ageInDays >= TILDE_WARNING_AGE_THRESHOLD[0] || ageInDays <= TILDE_WARNING_AGE_THRESHOLD[1]) && ageInDays !== 0){
    return "warning"
  }
  return "default"
};
