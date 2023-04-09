// TODO: implement as much server side rendering as possible. There is more to be done here

import Page from "../../../../components/LoggedInPage";

import { useRouter } from "next/router";
import {
  useFinishStep,
  useSubmitStepProjectLink,
  serverSideGetStepDetails,
  serverSideGetUserChallengeDetails,
  serverSideStartStep,
} from "../../../../apiHooks";

import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_READY,
  STATUS_UNDER_REVIEW,
  STATUS_ERROR,
} from "../../../../constants";

import { remark } from "remark";
import html from "remark-html";
import matter from "gray-matter";
import Presentation from "./[stepIndex].presentation";

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
