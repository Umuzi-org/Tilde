import { Title, Text, Stack, Loader, Group, Spoiler } from "@mantine/core";
import { STATUS_UNDER_REVIEW } from "../../../../../constants";

export default function ProjectReviews({ review, status }) {
  const showInProgress = status === STATUS_UNDER_REVIEW;
  const showEmpty = !review && !showInProgress;
  const showReview = !showInProgress && !showEmpty;

  return (
    <Stack spacing={"md"} mt="md">
      <Title order={3}>Feedback</Title>
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
        <Spoiler maxHeight={120} showLabel="Show more" hideLabel="Hide">
          {review.comments}
        </Spoiler>
      )}
    </Stack>
  );
}
