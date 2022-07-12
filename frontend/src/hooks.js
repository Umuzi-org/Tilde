import { useState, useEffect, useCallback } from "react";

export function useApiCallbacks({
  lastCallEntry,
  successResponseCallback,
  errorResponseCallback,
  finishedResponseCallback,
  startCallback,
}) {
  const [loading, setLoading] = useState(false);

  const handleSuccessResponse = useCallback(() => {
    if (successResponseCallback !== undefined) successResponseCallback();
  }, [successResponseCallback]);

  const handleFinished = useCallback(() => {
    if (finishedResponseCallback !== undefined) finishedResponseCallback();
  }, [finishedResponseCallback]);

  const handleErrorResponse = useCallback(() => {
    if (errorResponseCallback !== undefined) errorResponseCallback();
  }, [errorResponseCallback]);

  const handleStartCall = useCallback(() => {
    if (startCallback !== undefined) startCallback();
  }, [startCallback]);

  const callLogLoading = lastCallEntry && lastCallEntry.loading;
  const callLogResponseOk = lastCallEntry && lastCallEntry.responseOk;

  useEffect(() => {
    if (!loading & callLogLoading) {
      setLoading(true);
      handleStartCall();
    }
    if (loading & !callLogLoading) {
      setLoading(false);
      handleFinished();
      if (callLogResponseOk) {
        handleSuccessResponse();
      } else {
        handleErrorResponse();
      }
    }
  }, [
    callLogLoading,
    callLogResponseOk,
    handleErrorResponse,
    handleFinished,
    handleStartCall,
    handleSuccessResponse,
    loading,
  ]);
}
