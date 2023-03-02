import {
  Container,
  // Paper,
  Stack,
  Text,
  Title,
  // useMantineTheme,
  // Group,
  // RingProgress,
} from "@mantine/core";
import Page from "../../components/Page";

// import { statusLooks } from "../../brand";
import { steps } from "../../data";
import Step from "./components/Step";

export default function Home() {
  // const progressSections = Object.keys(statusLooks).map((STATUS) => {
  //   return {
  //     value:
  //       (100 / steps.length) *
  //       steps.filter((step) => step.status === STATUS).length,
  //     color: statusLooks[STATUS].color,
  //   };
  // });

  return (
    <Page>
      <Container>
        <Stack>
          <Title align="center">Challenge: Make a website</Title>

          <Text>
            In this challenge you'll learn the basics of web development and
            host your first website! You'll also learn about some of the best
            FREE learning resources around so you can continue learning on your
            own.
          </Text>

          {/* <RingProgress
            // roundCaps
            label={
              <Text size="xs" align="center">
                Progress
              </Text>
            }
            sections={progressSections}
          /> */}
          {steps.map((step, index) => (
            <Step
              key={index}
              number={index + 1}
              title={step.title}
              blurb={step.blurb}
              status={step.status}
            />
          ))}
        </Stack>
      </Container>
    </Page>
  );
}
