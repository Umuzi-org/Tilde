import type { AppProps } from "next/app";
import Head from "next/head";

import { MantineProvider } from "@mantine/core";

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
