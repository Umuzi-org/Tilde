import Page from "../../../../components/LoggedInPage";
import { Container, Title, Text, LoadingOverlay, Stack } from "@mantine/core";
import { useRouter } from "next/router";
import { useGetUserChallengeDetails } from "../../../../apiHooks";

import { Breadcrumbs } from "@mantine/core";

import Link from "next/link";

export default function ChallengeStep() {
  const router = useRouter();
  const getUserChallengeDetails = useGetUserChallengeDetails(router.query);

  const stepSummary = getUserChallengeDetails.responseData
    ? getUserChallengeDetails.responseData.steps[router.query.stepIndex]
    : {
        title: "Loading...",
        blurb: "Loading...",
      };

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
        <Stack>
          <Breadcrumbs>{crumbs}</Breadcrumbs>
          <div>
            <LoadingOverlay
              visible={getUserChallengeDetails.isLoading}
              overlayBlur={1}
              loaderProps={{ size: "xl" }}
            />
          </div>

          <Title>
            Step {parseInt(router.query.stepIndex) + 1}: {stepSummary.title}
          </Title>
          <Text>{stepSummary.blurb}</Text>
        </Stack>
      </Container>
    </Page>
  );
}
