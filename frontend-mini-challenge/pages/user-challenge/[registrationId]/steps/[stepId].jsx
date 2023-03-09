import { steps } from "../../../data";
import Page from "../../../components/Page";
import { Container, Title, Text } from "@mantine/core";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export default function ChallengeStep() {
  const router = useRouter();

  const [step, setStep] = useState({
    title: "Loading...",
    blurb: "Loading...",
    loading: true, //TODO - use this to show a loading overlay
  });

  useEffect(() => {
    const stepId = parseInt(router.query.stepId);
    if (stepId) setStep(steps[stepId]);
    // TODO: Handle missing step. 404
  }, [router.query]);

  console.log({ step });
  return (
    <Page>
      <Container>
        <Title>{step.title}</Title>
        <Text>{step.blurb}</Text>
      </Container>
    </Page>
  );
}
