import {
  Container,
  LoadingOverlay,
  AppShell,
  // Paper,
  // Stack,
  // Text,
  // Title,
  // useMantineTheme,
  // Group,
  // RingProgress,
} from "@mantine/core";
// import Page from "../components/LoggedInPage";
import { useEffect } from "react";
import { useWhoAmI, useGetUserActiveChallenges } from "../apiHooks";
import { getAuthToken } from "../lib/authTokenStorage";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const getWhoAmI = useWhoAmI();

  const getUserActiveChallenges = useGetUserActiveChallenges({
    user: getWhoAmI.status === 200 && getWhoAmI.responseData.userId,
  });

  console.log({ getUserActiveChallenges });

  useEffect(() => {
    const token = getAuthToken();

    if (!token) {
      console.log("no token. redirecting");
      router.push("/login");
      return;
    }

    if (getUserActiveChallenges.status === 200) {
      if (getUserActiveChallenges.responseData.length === 0) {
        router.push("/challenge-intro");
      } else {
        router.push("/challenge/TODO");
      }
    }
  }, [
    getUserActiveChallenges.responseData,
    getUserActiveChallenges.status,
    getWhoAmI.status,
    router,
  ]);

  return (
    <AppShell>
      <Container>
        <div>
          <LoadingOverlay
            visible={true}
            overlayBlur={1}
            loaderProps={{ size: "xl" }}
          />
        </div>
      </Container>
    </AppShell>
  );
}
