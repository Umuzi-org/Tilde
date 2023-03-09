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
import {
  useWhoAmI,
  useGetUserActiveChallenges,
  useRegisterForChallenge,
} from "../apiHooks";
import { getAuthToken } from "../lib/authTokenStorage";
import { useRouter } from "next/router";

const curriculum = 90; //

export default function Home() {
  const router = useRouter();
  const getWhoAmI = useWhoAmI();
  const getUserActiveChallenges = useGetUserActiveChallenges({
    user: getWhoAmI.status === 200 && getWhoAmI.responseData.userId,
  });
  const registerForChallenge = useRegisterForChallenge();

  useEffect(() => {
    const token = getAuthToken();

    if (!token) {
      console.log("no token. redirecting");
      router.push("/login");
      return;
    }

    if (
      getUserActiveChallenges.status === 200 &&
      getUserActiveChallenges.isLoading === false
    ) {
      if (
        getUserActiveChallenges.responseData.length === 0 &&
        registerForChallenge.isLoading === false &&
        registerForChallenge.status !== 201
      ) {
        // the user isn't registered for anything yet. Just sign them up
        registerForChallenge.call({
          user: getWhoAmI.responseData.userId,
          curriculum,
        });
      }
      if (getUserActiveChallenges.responseData.length === 1) {
        const registrationId = getUserActiveChallenges.responseData[0].id;
        router.push(`/user-challenge/${registrationId}`);
      }
      if (getUserActiveChallenges.responseData.length > 1) {
        console.log("TODO");
      }
    }
  }, [
    getUserActiveChallenges,
    getWhoAmI.responseData,
    getWhoAmI.status,
    registerForChallenge,
    router,
  ]);

  useEffect(() => {
    if (registerForChallenge.status === 201) getUserActiveChallenges.mutate();
  }, [getUserActiveChallenges, registerForChallenge.status]);

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
