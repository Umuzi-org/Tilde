import type { AppProps } from "next/app";
import Head from "next/head";

import { MantineProvider } from "@mantine/core";

import ErrorBoundary from "../components/ErrorBoundary";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MantineProvider
      withGlobalStyles
      withNormalizeCSS
      // theme={{ colorScheme: "dark" }}
    >
      <ErrorBoundary>
        <Head>
          <title>Coding challenge</title>
          <meta name="description" content="Coding challenge" />
          <link rel="icon" href="/favicon.png" />
        </Head>
        <Component {...pageProps} />
      </ErrorBoundary>
    </MantineProvider>
  );
}
