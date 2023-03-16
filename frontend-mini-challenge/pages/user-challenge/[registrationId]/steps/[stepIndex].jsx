// TODO: implement as much server side rendering as possible. There is more to be done here

import Page from "../../../../components/LoggedInPage";
import {
  Title,
  Text,
  LoadingOverlay,
  Stack,
  Loader,
  Group,
  Button,
  Breadcrumbs,
  Divider,
  Grid,
  Tooltip,
  Paper,
  Center,
} from "@mantine/core";
import { useRouter } from "next/router";
import {
  useGetUserChallengeDetails,
  // useStartStep,
  useFinishStep,
  useGetStepDetails,
  serverSideGetStepDetails,
  serverSideStartStep,
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

import { remark } from "remark";
import html from "remark-html";
import matter from "gray-matter";
import { ErrorAlert } from "../../../../components/Alerts";

export default function ChallengeStep({ contentHtml }) {
  const router = useRouter();
  const { stepIndex: stepIndexStr, registrationId: registrationIdStr } =
    router.query;

  const stepIndex = parseInt(stepIndexStr);
  const registrationId = parseInt(registrationIdStr);

  const getUserChallengeDetails = useGetUserChallengeDetails({
    registrationId,
  });

  // const startStep = useStartStep({ registrationId });
  const finishStep = useFinishStep({ registrationId });
  const getStepDetails = useGetStepDetails({ registrationId, stepIndex });

  const submitProjectLink = useSubmitStepProjectLink({
    registrationId,
  });

  function handleSubmitLinkForm({ linkSubmission }) {
    submitProjectLink.call({ linkSubmission, stepIndex });
  }

  const stepDetails = getStepDetails.responseData;
  console.log({ stepDetails });

  const registration = getUserChallengeDetails.responseData;
  const stepSummary = registration
    ? registration.steps[stepIndex]
    : {
        title: "Loading...",
        blurb: "Loading...",
      };

  useEffect(() => {
    getUserChallengeDetails.mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleNext() {
    if (stepSummary.status === STATUS_READY) {
      await finishStep.call({ index: stepIndex });
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

  const props = {
    registrationId,
    stepIndex,

    // TODO try simplify props by removing hook things. Just pass in what is strictly required
    getUserChallengeDetails,
    getStepDetails,
    submitProjectLink,

    registration,
    stepSummary,
    stepDetails,
    currentPath: router.asPath,
    contentHtml,

    handleNext,
    handlePrevious,
    handleSubmitLinkForm,
  };
  return <Presentation {...props} />;
}

function Presentation({
  registrationId,
  stepIndex,
  getUserChallengeDetails,
  getStepDetails,
  submitProjectLink,
  stepSummary,
  stepDetails,
  currentPath,
  contentHtml,
  registration,

  handleNext,
  handlePrevious,
  handleSubmitLinkForm,
}) {
  const isProject = stepDetails ? stepDetails.contentType === "P" : false;
  const nextIsBlockedByProject = isProject
    ? stepSummary.status !== STATUS_DONE
    : false;

  const nextButton = (
    <Button
      disabled={nextIsBlockedByProject || stepSummary.status === STATUS_BLOCKED}
      onClick={handleNext}
      rightIcon={<ForwardArrowIcon />}
    >
      {registration && stepIndex + 1 === registration.steps.length
        ? "Finish"
        : "Next"}
    </Button>
  );

  const { Icon, color } = stepSummary.status
    ? statusLooks[stepSummary.status]
    : {
        Icon: Loader,
        color: "",
      };

  const crumbs = [
    {
      title: getUserChallengeDetails.responseData
        ? getUserChallengeDetails.responseData.name
        : "Loading...",
      href: `/user-challenge/${registrationId}`,
    },
    { title: stepSummary.title, href: currentPath },
  ].map((item, index) => (
    <Link href={item.href} key={index}>
      {item.title}
    </Link>
  ));

  return (
    <Page>
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
              Step {parseInt(stepIndex) + 1}: {stepSummary.title}
            </Title>
          </Group>
          <Text mt="md" c="dimmed">
            {stepSummary.blurb}
          </Text>
        </div>

        {stepSummary.status === STATUS_BLOCKED ? (
          <Center>
            <Text>
              You can&apos;t do this step until you&apos;ve completed the last
              one
            </Text>
          </Center>
        ) : (
          <>
            <div style={{ position: "relative" }}>
              <LoadingOverlay
                visible={getStepDetails.isLoading}
                overlayBlur={1}
                loaderProps={{ size: "xl" }}
              />

              <Paper p="md" shadow="sm" withBorder>
                <div dangerouslySetInnerHTML={{ __html: contentHtml }} />
              </Paper>

              {isProject && (
                <Stack spacing={"md"} mt="md">
                  <Title order={2}>Project details</Title>
                  <Text>
                    This step is a project. That means you need to submit your
                    work before you can continue with the next step. Once you
                    have submitted your work you&apos;ll need to wait a little
                    while for us to mark it.
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
                        linkSubmission={stepDetails.linkSubmission}
                      />
                    </Grid.Col>
                    <Grid.Col span="auto">
                      <ProjectReviews reviews={stepDetails.reviews} />
                    </Grid.Col>
                  </Grid>
                </Stack>
              )}
            </div>
          </>
        )}

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
    </Page>
  );
}

export async function getServerSideProps({ query, req }) {
  const { stepIndex: stepIndexStr, registrationId: registrationIdStr } = query;
  const stepIndex = parseInt(stepIndexStr);
  const registrationId = parseInt(registrationIdStr);

  const startStepResponse = await serverSideStartStep({
    stepIndex,
    registrationId,
    req,
  });

  // TODO: consider upgrading to contentlayer later on.

  const stepDetails = await serverSideGetStepDetails({
    stepIndex,
    registrationId,
    req,
  });

  const raw_url = stepDetails.responseData.rawUrl;

  console.log({ stepDetails });
  // Fetch data from repo
  const res = await fetch(raw_url);

  const body = await res.text();
  const matterResult = matter(body);

  const processedContent = await remark()
    .use(html)
    .process(matterResult.content);
  const contentHtml = processedContent.toString();

  // Pass data to the page via props
  return { props: { contentHtml } };
}
