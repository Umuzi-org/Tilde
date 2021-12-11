const palette = {
  warning: "#ff9800",
  error: "#ef5350",
  default: "#212121",
};
const timeNow = new Date();
const milliseconds = 1000 * 60 * 60 * 24;
const timeDifferenceInDays = (time) => {
  return Math.ceil(Math.abs(timeNow - new Date(time)) / milliseconds);
};
let prColor;

export const getPrColor = (oldestOpenPrTime) => {
  if (timeDifferenceInDays(oldestOpenPrTime) === 1) {
    prColor = palette.default;
  } else if (timeDifferenceInDays(oldestOpenPrTime) <= 2) {
    prColor = palette.warning;
  } else {
    prColor = palette.error;
  }
  return prColor;
};

export const getTildeReviewColor = (oldestOpenPrTime) => {
  if (timeDifferenceInDays(oldestOpenPrTime) === 1) {
    prColor = palette.default;
  } else if (timeDifferenceInDays(oldestOpenPrTime) <= 3) {
    prColor = palette.warning;
  } else {
    prColor = palette.error;
  }
  return prColor;
};
