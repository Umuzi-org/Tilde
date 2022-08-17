import { useState, useEffect, useCallback, useRef } from "react";

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

/*This is useful for checking why a component re-renders.
eg usage:

function MyComponent({things,stuff}){
  useTraceUpdate({things,stuff})
  ...

}
*/
export function useTraceUpdate(props) {
  const prev = useRef(props);
  useEffect(() => {
    const changedProps = Object.entries(props).reduce((ps, [k, v]) => {
      if (prev.current[k] !== v) {
        ps[k] = [prev.current[k], v];
      }
      return ps;
    }, {});
    if (Object.keys(changedProps).length > 0) {
      console.log("Changed props:", changedProps);
    }
    prev.current = props;
  });
}
