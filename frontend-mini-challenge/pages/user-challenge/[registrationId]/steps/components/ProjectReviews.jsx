import {
  Title,
  Text,
  Stack,
  Loader,
  Group,
  Spoiler,
  Paper,
  ScrollArea,
} from "@mantine/core";
import {
  STATUS_UNDER_REVIEW,
  COMPETENT,
  NOT_YET_COMPETENT,
} from "../../../../../constants";
import { ReviewStatusLooks } from "../../../../../brand";

import { remark } from "remark";
import html from "remark-html";
import { useEffect, useState } from "react";
import { DateTime } from "../../../../../components/DateTime";

function useMarkdown(comments) {
  const [contentHtml, setContentHtml] = useState("");

  async function convertToHtml() {
    const processedContent = await remark().use(html).process(comments);
    setContentHtml(processedContent.toString());
  }

  return { contentHtml, convertToHtml };
}

function Review({ comments, status, timestamp }) {
  const { contentHtml, convertToHtml } = useMarkdown(comments);
  const { Icon, color, title } = ReviewStatusLooks[status];

  useEffect(() => {
    convertToHtml();
  }, [convertToHtml]);

  return (
    <>
      <Group>
        <Icon color={color} size="3rem" />
        <Title order={4}>{title} </Title>
        <DateTime timestamp={timestamp} />
      </Group>
      <Paper withBorder p="md">
        <div dangerouslySetInnerHTML={{ __html: contentHtml }} />
      </Paper>
    </>
  );
}

export default function ProjectReviews({ reviews, status }) {
  const showInProgress = status === STATUS_UNDER_REVIEW;
  const showEmpty = !reviews && !showInProgress;
  const showReview = !showInProgress && !showEmpty;

  return (
    <Stack spacing={"md"} mt="md">
      <Group>
        <Title order={3}>Feedback</Title>
      </Group>
      {showInProgress && (
        <>
          <Group position="center">
            <Text c="dimmed">
              Our trusty robot is busy reviewing your work...
            </Text>
          </Group>
          <Group position="center">
            <Loader variant="dots" />
          </Group>
          <Group position="center">
            <Text c="dimmed">
              Please REFRESH THE PAGE to see your feedback. Reviews take a few
              minutes. Once you have received a positive review you&apos;ll be
              able to move onto the next step
            </Text>
          </Group>
        </>
      )}
      {showEmpty && (
        <Group position="center">
          <Text c="dimmed">
            You have not received any reviews yet. Once you submit your project
            we will be able to review it.
          </Text>
        </Group>
      )}

      {showReview && (
        <ScrollArea h={250} type="always" scrollbarSize={12} pr="md">
          {reviews.map((review, index) => (
            <Review key={`review-${index}`} {...review} />
          ))}
        </ScrollArea>
      )}
    </Stack>
  );
}
