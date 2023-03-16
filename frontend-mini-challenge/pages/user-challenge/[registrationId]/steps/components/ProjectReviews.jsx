import { Title, Text, Stack, Loader, Group, Spoiler } from "@mantine/core";
import {
  STATUS_UNDER_REVIEW,
  COMPETENT,
  NOT_YET_COMPETENT,
} from "../../../../../constants";
import { ReviewStatusLooks } from "../../../../../brand";

export default function ProjectReviews({ review, status }) {
  const showInProgress = status === STATUS_UNDER_REVIEW;
  const showEmpty = !review && !showInProgress;
  const showReview = !showInProgress && !showEmpty;

  const reviewStatus = review && review.status;
  const { Icon: StatusIcon, color: reviewStatusColor } = ReviewStatusLooks[
    reviewStatus
  ] || { Icon: null, color: "" };

  return (
    <Stack spacing={"md"} mt="md">
      <Group>
        <Title order={3}>Feedback</Title>
        {showReview && <StatusIcon color={reviewStatusColor} size="3rem" />}
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
        <>
          <Spoiler maxHeight={120} showLabel="Show more" hideLabel="Hide">
            {review.comments}
          </Spoiler>
        </>
      )}
    </Stack>
  );
}
