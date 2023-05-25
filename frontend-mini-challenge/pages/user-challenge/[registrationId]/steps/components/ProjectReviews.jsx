import {
  Text,
  Stack,
  Loader,
  Group,
  Paper,
  ScrollArea,
  Divider,
} from "@mantine/core";
import { STATUS_UNDER_REVIEW } from "../../../../../constants";
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
      <Paper withBorder pl="md" pr="md" pt="md">
        <Group position="apart">
          <Group>
            <Icon color={color} size="2rem" />
            <Text>{title}</Text>
          </Group>
          <Text c="dimmed" fz="xs">
            <DateTime timestamp={timestamp} />
          </Text>
        </Group>
        <Divider mt="md" />
        <div dangerouslySetInnerHTML={{ __html: contentHtml }} />
      </Paper>
    </>
  );
}

export default function ProjectReviews({ reviews, status }) {
  const showInProgress = status === STATUS_UNDER_REVIEW;
  const showEmpty = reviews.length === 0 && !showInProgress;
  const showReviews = !showInProgress && !showEmpty;

  const olderReviews = reviews.slice(1);
  const firstReview = reviews[0];

  return (
    <Stack spacing={"md"} mt="md">
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
              Reviews take a few minutes to complete. Take a moment to reflect
              on what you have learned so far. Once you have received a positive
              review you&apos;ll be able to move onto the next step.
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

      {showReviews && (
        <ScrollArea h={250} type="always" scrollbarSize={12} pr="md">
          <Stack>
            {firstReview && <Review {...firstReview} />}
            {olderReviews.length > 0 && (
              <>
                <Divider label="Older reviews" labelPosition="center" />
                {olderReviews.map((review, index) => (
                  <Review key={`review-${index}`} {...review} />
                ))}
              </>
            )}
          </Stack>
        </ScrollArea>
      )}
    </Stack>
  );
}
