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
import { useWhoAmI } from "../apiHooks";
import { getAuthToken } from "../lib/authTokenStorage";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const { status } = useWhoAmI();

  useEffect(() => {
    const token = getAuthToken();

    if (!token) {
      console.log("no token. redirecting");
      router.push("/login");
      return;
    }

    if (status === 200) {
      router.push("/challenge");
    }
  });

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
