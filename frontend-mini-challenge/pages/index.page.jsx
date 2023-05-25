import { Container, LoadingOverlay, AppShell } from "@mantine/core";
import { useEffect } from "react";
import {
  useWhoAmI,
  useGetUserActiveChallenges,
  useRegisterForChallenge,
} from "../apiHooks";
import { getAuthToken } from "../lib/authTokenStorage";
import { useRouter } from "next/router";
import { useState } from "react";

const curriculum = 90; // TODO. When we have more challenges we wont be able to hard-code this value

export default function Home() {
  const router = useRouter();
  const getWhoAmI = useWhoAmI();

  const getUserActiveChallenges = useGetUserActiveChallenges({
    user: getWhoAmI.status === 200 && getWhoAmI.responseData.userId,
  });
  const registerForChallenge = useRegisterForChallenge();

  const [calledPush, setCalledPush] = useState(false);

  useEffect(() => {
    function routerPushOnce(path) {
      if (calledPush) return;
      setCalledPush(true);
      router.push(path);
    }
    const token = getAuthToken();

    if (!token) {
      console.log("no token. redirecting");
      routerPushOnce("/login");
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
        routerPushOnce(`/user-challenge/${registrationId}`);
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
    calledPush,
    setCalledPush,
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
