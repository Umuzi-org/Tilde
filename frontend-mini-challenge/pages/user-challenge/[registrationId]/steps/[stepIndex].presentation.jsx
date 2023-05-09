import {
  Title,
  Text,
  Stack,
  Loader,
  Group,
  Button,
  Divider,
  Grid,
  Tooltip,
  Paper,
  Center,
  Tabs,
  MediaQuery,
} from "@mantine/core";
import {
  BackArrowIcon,
  ForwardArrowIcon,
  statusLooks,
  ProjectIcon,
  ContentIcon,
} from "../../../../brand";

import { Bold } from "../../../../components/Text";

import Link from "next/link";
import ProjectReviews from "./components/ProjectReviews";
import LinkForm from "./components/LinkForm";

import { InfoAlert } from "../../../../components/Alerts";

import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_ERROR,
  STATUS_UNDER_REVIEW,
} from "../../../../constants";

function ContentHtml({ contentHtml }) {
  return (
    <Paper p="md" shadow="sm" withBorder style={{ overflowX: "scroll" }}>
      <div
        dangerouslySetInnerHTML={{ __html: contentHtml }}
        // style={{ width: "100%" }}
      />
    </Paper>
  );
}

function ProjectSmallDeviceLayout({
  contentHtml,
  stepDetails,
  handleSubmitLinkForm,
  submitProjectLink,
}) {
  const tabValues = {
    content: "content",
    project: "project",
  };
  const defaultTab = [STATUS_ERROR, STATUS_UNDER_REVIEW].includes(
    stepDetails.status
  )
    ? tabValues.project
    : tabValues.content;

  return (
    <>
      <InfoAlert Icon={ProjectIcon}>
        <Stack spacing="xs">
          <Text>
            This step is a <Bold>Project</Bold>, that means that you are going
            to need to hand in some homework. Once you have handed in then we
            will mark your work. You will either pass or fail.
          </Text>
          <Text>
            If you <Bold>fail</Bold> then try not to stress out, you can try
            again as many times as you need to! Try to learn from the feedback.
          </Text>
          <Text>
            <Bold>
              You will only be allowed to go onto the next step once you have
              passed.
            </Bold>
          </Text>

          <Text>
            Click on the <ProjectIcon /> Project tab below to submit your work
            and see feedback
          </Text>
        </Stack>
      </InfoAlert>
      <Tabs defaultValue={defaultTab}>
        <Tabs.List>
          <Tabs.Tab value={tabValues.content} icon={<ContentIcon />}>
            Content
          </Tabs.Tab>
          <Tabs.Tab value={tabValues.project} icon={<ProjectIcon />}>
            Project
          </Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value={tabValues.content}>
          <ContentHtml contentHtml={contentHtml} />
        </Tabs.Panel>
        <Tabs.Panel value={tabValues.project} pt="xs">
          <Stack spacing={"md"} mt="md">
            <Grid>
              <Grid.Col xs="auto" sm={4} md={3} lg={3} xl={3}>
                <Center>
                  <Title order={3}>Project submission</Title>
                </Center>

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
                <Center>
                  <Title order={3}>Feedback</Title>
                </Center>
                <ProjectReviews
                  reviews={stepDetails.reviews}
                  status={stepDetails.status}
                />
              </Grid.Col>
            </Grid>
          </Stack>
        </Tabs.Panel>
      </Tabs>
      {/* 


      </Tabs> */}
    </>
  );
}

function TopicLayout({ contentHtml }) {
  return <ContentHtml contentHtml={contentHtml} />;
}

export default function Presentation({
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
  const isProject = stepDetails ? stepDetails.contentType === "P" : false;
  const isTopic = stepDetails ? stepDetails.contentType === "T" : false;

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

  // const crumbs = [
  //   {
  //     title: registration.name,
  //     href: `/user-challenge/${registrationId}`,
  //   },
  //   { title: stepDetails.title, href: currentPath },
  // ].map((item, index) => (
  //   <Link href={item.href} key={index}>
  //     {item.title}
  //   </Link>
  // ));

  return (
    <>
      <Stack spacing={"md"}>
        <Link href={`/user-challenge/${registrationId}`}>
          <Text fz="sm" c="dimmed">
            Back to challenge
          </Text>
        </Link>
        <MediaQuery smallerThan="sm" styles={{ display: "none" }}>
          <Group spacing="xs">
            <Icon size="4rem" color={color} />
            <Title>Step {parseInt(stepIndex) + 1}.</Title>
            <Title>{stepDetails.title}</Title>
          </Group>
        </MediaQuery>

        <MediaQuery largerThan="sm" styles={{ display: "none" }}>
          <Group spacing="xs">
            <Icon size="2.5rem" color={color} />
            <Title size="1.5rem">Step {parseInt(stepIndex) + 1}.</Title>
            <Title size="1.5rem">{stepDetails.title}</Title>
          </Group>
        </MediaQuery>

        <Text mt="md" c="dimmed">
          {stepDetails.blurb}
        </Text>

        {stepDetails.status === STATUS_BLOCKED ? (
          <Center>
            <Text>
              You can&apos;t do this step until you&apos;ve completed the last
              one
            </Text>
          </Center>
        ) : (
          <>
            {isTopic && <TopicLayout contentHtml={contentHtml} />}
            {isProject && (
              <ProjectSmallDeviceLayout
                contentHtml={contentHtml}
                stepDetails={stepDetails}
                handleSubmitLinkForm={handleSubmitLinkForm}
                submitProjectLink={submitProjectLink}
              />
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
    </>
  );
}
