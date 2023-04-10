import { Stack, Text, Title } from "@mantine/core";
import Page, {
  getServerSidePropsForLoggedInPage,
} from "../../../components/LoggedInPage";

import Step from "./components/Step";

import { serverSideGetUserChallengeDetails } from "../../../apiHooks";

export default function ChallengeRegistration({
  loggedInPageProps,
  challengeDetails,
}) {
  return (
    <Page {...loggedInPageProps}>
      {loggedInPageProps.isLoggedIn && (
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
      )}
    </Page>
  );
}

export async function getServerSideProps({ query, req }) {
  const loggedInPageProps = await getServerSidePropsForLoggedInPage({
    query,
    req,
  });

  const { registrationId: registrationIdStr } = query;
  const registrationId = parseInt(registrationIdStr);

  let challengeDetails = null;

  if (loggedInPageProps.isLoggedIn) {
    const challengeDetailsResponse = await serverSideGetUserChallengeDetails({
      registrationId,
      req,
    });
    challengeDetails = challengeDetailsResponse.responseData;
  }

  return {
    props: {
      loggedInPageProps,
      challengeDetails,
    },
  };
}
