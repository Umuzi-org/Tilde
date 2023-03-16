import { Container, Stack, Text, Title, LoadingOverlay } from "@mantine/core";
import Page from "../../../components/LoggedInPage";

import Step from "./components/Step";

import { useGetUserChallengeDetails } from "../../../apiHooks";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const getUserChallengeDetails = useGetUserChallengeDetails(router.query);

  const challengeDetails = getUserChallengeDetails.responseData || {
    steps: [],
  };

  return (
    <Page>
      <div>
        <LoadingOverlay
          visible={getUserChallengeDetails.isLoading}
          overlayBlur={1}
          loaderProps={{ size: "xl" }}
        />
      </div>
      <Stack>
        <Title align="center">{challengeDetails.name}</Title>

        <Text>{challengeDetails.blurb}</Text>

        {challengeDetails.steps.map((step, index) => (
          <Step
            key={index}
            index={index}
            title={step.title}
            blurb={step.blurb}
            status={step.status}
          />
        ))}
      </Stack>
    </Page>
  );
}
