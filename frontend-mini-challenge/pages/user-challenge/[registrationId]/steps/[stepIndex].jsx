// TODO: implement as much server side rendering as possible. There is more to be done here

import Page from "../../../../components/LoggedInPage";
import {
  Title,
  Text,
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
  useFinishStep,
  useSubmitStepProjectLink,
  serverSideGetStepDetails,
  serverSideGetUserChallengeDetails,
  serverSideStartStep,
} from "../../../../apiHooks";
import {
  BackArrowIcon,
  ForwardArrowIcon,
  statusLooks,
} from "../../../../brand";

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

export default function ChallengeStep({
  contentHtml,
  registration,
  stepDetails,
}) {
  const router = useRouter();
  const { stepIndex: stepIndexStr, registrationId: registrationIdStr } =
    router.query;

  const stepIndex = parseInt(stepIndexStr);
  const registrationId = parseInt(registrationIdStr);

  const finishStep = useFinishStep({ registrationId });

  const submitProjectLink = useSubmitStepProjectLink({
    registrationId,
    stepIndex,
  });

  async function handleSubmitLinkForm({ linkSubmission }) {
    await submitProjectLink.call({ linkSubmission });
  }

  async function handleNext() {
    if (stepDetails.status === STATUS_READY) {
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

  const currentPath = router.asPath;
  const props = {
    contentHtml,
    registrationId,
    stepIndex,

    registration,
    stepDetails,

    submitProjectLink,
    currentPath,

    handleNext,
    handlePrevious,
    handleSubmitLinkForm,
  };
  return (
    <Page>
      <Presentation {...props} />
    </Page>
  );
}

export function Presentation({
  contentHtml,
  registrationId,
  stepIndex,

  registration,
  stepDetails,

  submitProjectLink,
  currentPath,

  handleNext,
  handlePrevious,
  handleSubmitLinkForm,
}) {
  console.log({
    contentHtml,
    registrationId,
    stepIndex,

    registration,
    stepDetails,

    submitProjectLink,
    currentPath,
  });

  const isProject = stepDetails ? stepDetails.contentType === "P" : false;

  const nextIsBlockedByProject = isProject
    ? stepDetails.status !== STATUS_DONE
    : false;

  const nextButton = (
    <Button
      disabled={nextIsBlockedByProject || stepDetails.status === STATUS_BLOCKED}
      onClick={handleNext}
      rightIcon={<ForwardArrowIcon />}
    >
      {stepIndex + 1 === registration.steps.length ? "Finish" : "Next"}
    </Button>
  );

  const { Icon, color } = stepDetails.status
    ? statusLooks[stepDetails.status]
    : {
        Icon: Loader,
        color: "",
      };

  const crumbs = [
    {
      title: registration.name,
      href: `/user-challenge/${registrationId}`,
    },
    { title: stepDetails.title, href: currentPath },
  ].map((item, index) => (
    <Link href={item.href} key={index}>
      {item.title}
    </Link>
  ));

  return (
    <Stack spacing={"md"}>
      <Breadcrumbs>{crumbs}</Breadcrumbs>

      <Group>
        <Icon size="4rem" color={color} />
        <Title>
          Step {parseInt(stepIndex) + 1}: {stepDetails.title}
        </Title>
      </Group>
      <Text mt="md" c="dimmed">
        {stepDetails.blurb}
      </Text>

      {stepDetails.status === STATUS_BLOCKED ? (
        <Center>
          <Text>
            You can&apos;t do this step until you&apos;ve completed the last one
          </Text>
        </Center>
      ) : (
        <>
          <Paper p="md" shadow="sm" withBorder>
            <div dangerouslySetInnerHTML={{ __html: contentHtml }} />
          </Paper>

          {isProject && (
            <Stack spacing={"md"} mt="md">
              <Title order={2}>Project details</Title>
              <Text>
                This step is a project. That means you need to submit your work
                before you can continue with the next step. Once you have
                submitted your work you&apos;ll need to wait a little while for
                us to mark it.
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
                  <ProjectReviews
                    reviews={stepDetails.reviews}
                    status={stepDetails.status}
                  />
                </Grid.Col>
              </Grid>
            </Stack>
          )}
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

  const rawUrl = stepDetails.responseData.rawUrl;

  // Fetch data from repo
  const res = await fetch(rawUrl);

  const body = await res.text();
  const matterResult = matter(body);

  const processedContent = await remark()
    .use(html)
    .process(matterResult.content);
  const contentHtml = processedContent.toString();

  const registration = await serverSideGetUserChallengeDetails({
    registrationId,
    req,
  });

  return {
    props: {
      contentHtml,
      registration: registration.responseData,
      stepDetails: stepDetails.responseData,
    },
  };
}
