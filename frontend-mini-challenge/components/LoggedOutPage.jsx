// TODO: make sure it's responsive: https://mantine.dev/core/app-shell/

import { AppShell, Container, Header } from "@mantine/core";
import { useWhoAmI } from "../apiHooks";
import { useEffect } from "react";
import { useRouter } from "next/router";
import logger from "../logger";

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

  const router = useRouter();

  useEffect(() => {
    if (whoAmIStatus === 200) {
      console.log("WHO AM I 200. redirecting");
      router.push("/");
      return;
    }
  });

  return <Presentation>{children}</Presentation>;
}

export function Presentation({ children }) {
  return (
    <AppShell padding="md" header={<Header height={60} p="xs"></Header>}>
      <Container>{children}</Container>
    </AppShell>
  );
}

export async function getServerSidePropsForLoggedOutPage({ req }) {
  const { url } = req;
  logger.http({ user_id: null, url }, `Page access`);

  return {
    serverSidePropsCorrectlyCalled: true,
  };
}
