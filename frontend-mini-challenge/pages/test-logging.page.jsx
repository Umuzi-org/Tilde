import { useEffect } from "react";
import logger from "../logger";

const stackTrace = `at Login (webpack-internal:///./pages/login/index.page.jsx:32:11)
at ErrorBoundary (webpack-internal:///./components/ErrorBoundary.jsx:94:9)
at ThemeProvider (webpack-internal:///./node_modules/@emotion/react/dist/emotion-element-c39617d8.browser.esm.js:123:50)
at MantineProvider (webpack-internal:///./node_modules/@mantine/styles/esm/theme/MantineProvider.js:78:3)
at App (webpack-internal:///./pages/_app.page.tsx:16:11)
at PathnameContextProviderAdapter (webpack-internal:///./node_modules/next/dist/shared/lib/router/adapters.js:74:11)
at ErrorBoundary (webpack-internal:///./node_modules/next/dist/compiled/@next/react-dev-overlay/dist/client.js:305:63)
at ReactDevOverlay (webpack-internal:///./node_modules/next/dist/compiled/@next/react-dev-overlay/dist/client.js:854:919)
at Container (webpack-internal:///./node_modules/next/dist/client/index.js:77:1)
at AppContainer (webpack-internal:///./node_modules/next/dist/client/index.js:181:11)
at Root (webpack-internal:///./node_modules/next/dist/client/index.js:359:11)`;

export default function TestLogging() {
  logger.debug("client-side debug");
  logger.info("client-side info");
  logger.notice("client-side notice");
  logger.warn("client-side warn");
  logger.error("client-side error");
  logger.crit("client-side crit");
  logger.alert("client-side alert");
  logger.emerg("client-side emerg");

  logger.error(
    { data: "structured data", stack_trace: stackTrace },
    "client-side error with structured data"
  );

  useEffect(() => {
    console.log(" --------- useEffect ----------");
    logger.debug("useEffect debug");
    logger.info("useEffect info");
    logger.warn("useEffect warn");
    logger.error("useEffect error");
    console.log(" --------- useEffect end ----------");
  }, []);

  return <div>TestLogging</div>;
}

export async function getServerSideProps({ req }) {
  logger.debug("server-side debug");
  logger.info("server-side info");
  logger.warn("server-side warn");
  logger.error("server-side error");
  return { props: {} };
}
