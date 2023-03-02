// TODO: make sure it's responsive: https://mantine.dev/core/app-shell/

import { AppShell, Header } from "@mantine/core";
import { useWhoAmI } from "../apiHooks";
import { useEffect } from "react";
import { useRouter } from "next/router";

export default function Page({ children }) {
  const {
    jsonData: userData,
    isLoading: isLoadingWhoAmI,
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

  return (
    <AppShell padding="md" header={<Header height={60} p="xs"></Header>}>
      {children}
    </AppShell>
  );
}
