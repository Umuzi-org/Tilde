import Page from "../../../../components/LoggedInPage";
import {
  Container,
  Title,
  Text,
  LoadingOverlay,
  Stack,
  Loader,
  Group,
  Paper,
  Button,
  Breadcrumbs,
} from "@mantine/core";
import { useRouter } from "next/router";
import {
  useGetUserChallengeDetails,
  useStartStep,
  useFinishStep,
} from "../../../../apiHooks";
import { statusLooks } from "../../../../brand";
import { useEffect } from "react";
// import { useForm } from "@mantine/form";

import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_READY,
  STATUS_UNDER_REVIEW,
  STATUS_ERROR,
} from "../../../../constants";

import Link from "next/link";

export default function ChallengeStep() {
  const router = useRouter();
  const { stepIndex, registrationId } = router.query;

  const getUserChallengeDetails = useGetUserChallengeDetails({
    registrationId,
  });
  const startStep = useStartStep({ registrationId });
  const finishStep = useFinishStep({ registrationId });

  const registration = getUserChallengeDetails.responseData;
  const stepSummary = registration
    ? registration.steps[stepIndex]
    : {
        title: "Loading...",
        blurb: "Loading...",
      };

  useEffect(() => {
    if (stepIndex !== undefined && registration) {
      if (stepSummary.status === STATUS_READY && !startStep.status)
        // TODO: debounce. This gets called twice.
        startStep.call({ index: stepIndex });
    }
  }, [
    registration,
    router.query.stepIndex,
    startStep,
    stepIndex,
    stepSummary.status,
  ]);

  const { Icon, color } = stepSummary.status
    ? statusLooks[stepSummary.status]
    : {
        Icon: Loader,
        color: "",
      };

  function handleNext() {
    finishStep.call({ index: stepIndex });
    getUserChallengeDetails.mutate();
  }

  const crumbs = [
    {
      title: getUserChallengeDetails.responseData
        ? getUserChallengeDetails.responseData.name
        : "Loading...",
      href: `/user-challenge/${router.query.registrationId}`,
    },
    { title: stepSummary.title, href: router.asPath },
  ].map((item, index) => (
    <Link href={item.href} key={index}>
      {item.title}
    </Link>
  ));

  return (
    <Page>
      <Container>
        <Stack spacing={"md"}>
          <Breadcrumbs>{crumbs}</Breadcrumbs>
          <div style={{ position: "relative" }}>
            <LoadingOverlay
              visible={getUserChallengeDetails.isLoading}
              overlayBlur={1}
              loaderProps={{ size: "xl" }}
            />
            <Group>
              <Icon size="4rem" color={color} />
              <Title>
                Step {parseInt(router.query.stepIndex) + 1}: {stepSummary.title}
              </Title>
            </Group>
            <Text mt="md" c="dimmed">
              {stepSummary.blurb}
            </Text>
          </div>

          <Paper shadow="xs" p="md">
            TODO: figure out how to actually display the content.
          </Paper>

          <Button>Update Link</Button>
          <Button onClick={handleNext}>Next</Button>
          <Button>Finished!</Button>
          <Button>Previous</Button>
        </Stack>
      </Container>
    </Page>
  );
}
