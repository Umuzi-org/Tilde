import { useState } from "react";

export default function useOpenAndCloseReviewPopUp() {
  const [openReviewPopUp, setOpenReviewPopUp] = useState(false);
  return {
    openReviewPopUp,
    setOpenReviewPopUp,
  }
}
