const palette = {
  warning: "#ff9800",
  error: "#ef5350",
  default: "#212121",
};

export const timeDifferenceInDays = (time) => {
  return Math.ceil(Math.abs(new Date() - new Date(time)) / (1000 * 60 * 60 * 24));
};

export const getPrColor = (oldestOpenPrTime) => {
  let prColor;
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
  let tildeReviewColor
  if (timeDifferenceInDays(oldestOpenPrTime) === 1) {
    tildeReviewColor = palette.default;
  } else if (timeDifferenceInDays(oldestOpenPrTime) <= 3) {
    tildeReviewColor = palette.warning;
  } else {
    tildeReviewColor = palette.error;
  }
  return tildeReviewColor;
};
