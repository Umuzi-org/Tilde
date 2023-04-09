// TODO: implement as much server side rendering as possible. There is more to be done here

import Page, {
  getServerSidePropsForLoggedInPage,
} from "../../../../components/LoggedInPage";

import { useRouter } from "next/router";
import {
  useFinishStep,
  useSubmitStepProjectLink,
  serverSideGetStepDetails,
  serverSideGetUserChallengeDetails,
  useRefreshReviewStepDetails,
  serverSideStartStep,
  delay,
} from "../../../../apiHooks";

import { STATUS_READY, STATUS_UNDER_REVIEW } from "../../../../constants";

import { remark } from "remark";
import html from "remark-html";
import matter from "gray-matter";
import Presentation from "./[stepIndex].presentation";
import { useEffect, useState } from "react";

export default function ChallengeStep({
  contentHtml,
  registration,
  stepDetails,
  loggedInPageProps,
  stepIndex,
  registrationId,
}) {
  const router = useRouter();

  const finishStep = useFinishStep({ registrationId });

  const submitProjectLink = useSubmitStepProjectLink({
    registrationId,
    stepIndex,
  });

  const [currentStepStatus, setCurrentStepStatus] = useState(
    stepDetails.status
  );

  // console.log({ submitProjectLink, currentStepStatus });
  const stepDetailsClientSideRefreshed = useRefreshReviewStepDetails({
    registrationId,
    stepIndex,
    currentStepStatus,
  });

  const [finalStepDetails, setFinalStepDetails] = useState(stepDetails);

  useEffect(() => {
    if (
      stepDetailsClientSideRefreshed &&
      stepDetailsClientSideRefreshed.responseData
    ) {
      console.log({
        refreshedStep: stepDetailsClientSideRefreshed.responseData,
      });
      setCurrentStepStatus(stepDetailsClientSideRefreshed.responseData.status);
      setFinalStepDetails(stepDetailsClientSideRefreshed.responseData);
    }
  }, [stepDetailsClientSideRefreshed]);

  /* Whenever we submit a project link then we set the status to reviewing.
  When the status is STATUS_UNDER_REVIEW then the refresher will constantly refetch
  */
  useEffect(() => {
    if (
      submitProjectLink.isLoading === false &&
      submitProjectLink.status === 200
    ) {
      setCurrentStepStatus(STATUS_UNDER_REVIEW);
      // there is a race condition. when submitting a link for review then
      // the step doesn't always get the review status.
      // TODO: make sure we aren't making duplicate calls
      delay(2000).then(() => setCurrentStepStatus(STATUS_UNDER_REVIEW));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [submitProjectLink.isLoading]);

  async function handleSubmitLinkForm({ linkSubmission }) {
    submitProjectLink.call({ linkSubmission });
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
    stepDetails: finalStepDetails,

    submitProjectLink,
    currentPath,

    handleNext,
    handlePrevious,
    handleSubmitLinkForm,
  };
  return (
    <Page {...loggedInPageProps}>
      {loggedInPageProps.isLoggedIn && <Presentation {...props} />}
    </Page>
  );
}

export async function getServerSideProps({ query, req }) {
  const { stepIndex: stepIndexStr, registrationId: registrationIdStr } = query;
  const stepIndex = parseInt(stepIndexStr);
  const registrationId = parseInt(registrationIdStr);

  const loggedInPageProps = await getServerSidePropsForLoggedInPage({
    query,
    req,
  });

  let stepDetails = null;
  let registration = null;
  let contentHtml = null;

  if (loggedInPageProps.isLoggedIn) {
    await serverSideStartStep({
      stepIndex,
      registrationId,
      req,
    });

    // TODO: consider upgrading to contentlayer later on.

    const stepDetailsResponse = await serverSideGetStepDetails({
      stepIndex,
      registrationId,
      req,
    });

    stepDetails = stepDetailsResponse.responseData;

    const rawUrl = stepDetails.rawUrl;

    // Fetch data from repo
    const res = await fetch(rawUrl);
    const body = await res.text();
    const matterResult = matter(body);

    const processedContent = await remark()
      .use(html)
      .process(matterResult.content);
    contentHtml = processedContent.toString();

    const registrationResponse = await serverSideGetUserChallengeDetails({
      registrationId,
      req,
    });

    registration = registrationResponse.responseData;
  }

  return {
    props: {
      contentHtml,
      registration,
      stepDetails,
      loggedInPageProps,
      stepIndex,
      registrationId,
    },
  };
}
