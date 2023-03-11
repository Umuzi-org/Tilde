import Page from "../../../../components/LoggedInPage";
import {
  Container,
  Title,
  Text,
  LoadingOverlay,
  Stack,
  Loader,
  Group,
  Button,
  Breadcrumbs,
  Box,
  Divider,
  Center,
  Grid,
  Tooltip,
} from "@mantine/core";
import { useRouter } from "next/router";
import {
  useGetUserChallengeDetails,
  useStartStep,
  useFinishStep,
  useGetStepDetails,
  useSubmitStepProjectLink,
} from "../../../../apiHooks";
import {
  BackArrowIcon,
  ForwardArrowIcon,
  statusLooks,
} from "../../../../brand";
import { useEffect } from "react";

import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_READY,
  STATUS_UNDER_REVIEW,
  STATUS_ERROR,
} from "../../../../constants";

import Link from "next/link";
import ProjectReviews from "./components/ProjectReviews";
import LinkForm from "./components/LinkForm";

export default function ChallengeStep() {
  const router = useRouter();
  const { stepIndex: stepIndexStr, registrationId: registrationIdStr } =
    router.query;

  const stepIndex = parseInt(stepIndexStr);
  const registrationId = parseInt(registrationIdStr);

  const getUserChallengeDetails = useGetUserChallengeDetails({
    registrationId,
  });
  const startStep = useStartStep({ registrationId });
  const finishStep = useFinishStep({ registrationId });
  const getStepDetails = useGetStepDetails({ registrationId, stepIndex });

  const submitProjectLink = useSubmitStepProjectLink({
    registrationId,
  });

  function handleSubmitLinkForm({ linkSubmission }) {
    call({ linkSubmission, stepIndex });
  }

  const stepDetails = getStepDetails.responseData;

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
    if (stepSummary.status === STATUS_READY) {
      finishStep.call({ index: stepIndex });
      getUserChallengeDetails.mutate();
    }
    if (stepIndex + 1 === registration.steps.length) {
      router.push(`/user-challenge/${registrationId}`);
    } else {
      router.push(`/user-challenge/${registrationId}/steps/${stepIndex + 1}`);
    }
  }

  function handlePrevious() {
    if (stepIndex > 0)
      router.push(`/user-challenge/${registrationId}/steps/${stepIndex - 1}`);
    else router.push(`/user-challenge/${registrationId}/`);
  }

  const showFinishButton = registration
    ? stepIndex + 1 === registration.steps.length
    : false;
  const showNextButton = registration ? !showFinishButton : false;

  const showLinkForm = stepDetails
    ? stepDetails.contentType === "P" &&
      stepDetails.projectSubmissionType === "L"
    : false;

  const isProject = stepDetails ? stepDetails.contentType === "P" : false;

  const nextIsBlockedByProject = isProject
    ? stepDetails.status !== STATUS_DONE
    : false;

  const nextButton = (
    <Button
      disabled={nextIsBlockedByProject}
      onClick={handleNext}
      rightIcon={<ForwardArrowIcon />}
    >
      {registration && stepIndex + 1 === registration.steps.length
        ? "Finish"
        : "Next"}
    </Button>
  );
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

          <div style={{ position: "relative" }}>
            <LoadingOverlay
              visible={getStepDetails.isLoading}
              overlayBlur={1}
              loaderProps={{ size: "xl" }}
            />

            <Box mt="md">
              <Text>
                The content for this step can be found at the following link.
                Please follow the instructions in link and come back here when
                you are done
              </Text>
              <Center>
                <a href={stepDetails && stepDetails.url} target="_blank">
                  <Text fz="xl">View content</Text>
                </a>
              </Center>
            </Box>

            {isProject && (
              <>
                <Divider mt="md" />

                <Stack spacing={"md"} mt="md">
                  <Title order={2}>Project details</Title>
                  <Text>
                    This step is a project. That means you need to submit your
                    work before you can continue with the next step. Once you
                    have submitted your work you'll need to wait a little while
                    for us to mark it.
                  </Text>
                  <Grid>
                    <Grid.Col span="auto">
                      <LinkForm
                        linkExample={stepDetails.linkExample}
                        linkName={stepDetails.linkName}
                        handleSubmit={handleSubmitLinkForm}
                        status={submitProjectLink.status}
                        responseData={submitProjectLink.responseData}
                        isLoading={submitProjectLink.isLoading}
                      />
                    </Grid.Col>
                    <Grid.Col span="auto">
                      <ProjectReviews reviews={stepDetails.reviews} />
                    </Grid.Col>
                  </Grid>
                </Stack>
              </>
            )}
          </div>
          <Divider mt="md" />
          <Group position="apart">
            <Button onClick={handlePrevious} leftIcon={<BackArrowIcon />}>
              Back
            </Button>

            {nextIsBlockedByProject ? (
              <Tooltip label="You wont be able to go to the next step until you have submitted a passing project">
                {nextButton}
              </Tooltip>
            ) : (
              nextButton
            )}
          </Group>
        </Stack>
      </Container>
    </Page>
  );
}
