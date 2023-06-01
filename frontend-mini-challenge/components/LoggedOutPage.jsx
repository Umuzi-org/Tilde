// TODO: make sure it's responsive: https://mantine.dev/core/app-shell/

import { AppShell, Container, Header } from "@mantine/core";
import { useWhoAmI } from "../apiHooks";
import { useEffect } from "react";
import { useRouter } from "next/router";
import logger from "../logger";
// import { useState } from "react";

export default function Page({ children, serverSidePropsCorrectlyCalled }) {
  if (!serverSidePropsCorrectlyCalled) {
    throw new Error(
      "It looks like you didn't make use of the getServerSideProps function defined below"
    );
  }

  const {
    // responseData: userData,
    // isLoading: isLoadingWhoAmI,
    status: whoAmIStatus,
  } = useWhoAmI();
  // const [loggedPageVisit, setLoggedPageVisit] = useState(false);

  const router = useRouter();
  const url = router.asPath;

  // useEffect(() => {
  //   if (loggedPageVisit) return;
  //   setLoggedPageVisit(true);
  //   logger.http({ user_id: null, url }, `Page access`);
  // }, [loggedPageVisit, url]);

  useEffect(() => {
    if (whoAmIStatus === 200) {
      console.log("WHO AM I 200. redirecting");
      router.push("/");
      return;
    }
  });

  return (
    <AppShell padding="md" header={<Header height={60} p="xs"></Header>}>
      <Container>{children}</Container>
    </AppShell>
  );
}

export async function getServerSidePropsForLoggedOutPage({ query, req }) {
  const { url } = req;
  logger.http({ user_id: null, url }, `Page access`);

  return {
    serverSidePropsCorrectlyCalled: true,
  };
}
