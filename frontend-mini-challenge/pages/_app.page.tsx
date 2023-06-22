import type { AppProps } from "next/app";
import Head from "next/head";

import { MantineProvider } from "@mantine/core";

// you can import these packages anywhere
const LogRocket = require("logrocket");
const setupLogRocketReact = require("logrocket-react");

// only initialize when in the browser
if (typeof window !== "undefined") {
  LogRocket.init("b4pgma/waypoints");
  // plugins should also only be initialized when in the browser
  setupLogRocketReact(LogRocket);
}

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Coding challenge</title>
        <meta name="description" content="Coding challenge" />
        <link rel="icon" href="/favicon.png" />
      </Head>
      <MantineProvider
        withGlobalStyles
        withNormalizeCSS
        // theme={{ colorScheme: "dark" }}
      >
        <Component {...pageProps} />
      </MantineProvider>
    </>
  );
}
