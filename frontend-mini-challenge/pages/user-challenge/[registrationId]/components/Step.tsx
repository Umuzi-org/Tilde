import {
  Paper,
  Stack,
  Text,
  Title,
  useMantineTheme,
  Group,
  Tooltip,
} from "@mantine/core";

import { statusLooks } from "../../../../brand";
import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_READY,
  STATUS_UNDER_REVIEW,
  STATUS_ERROR,
} from "../../../../constants";
import { useRouter } from "next/router";
import Link from "next/link";

export default function Step({ index, title, blurb, status }) {
  const router = useRouter();

  const theme = useMantineTheme();
  console.log({ statusLooks, status });
  const { Icon, color } = statusLooks[status];

  const styles = {
    [STATUS_BLOCKED]: {
      cursor: "not-allowed",
    },
    [STATUS_DONE]: {
      cursor: "pointer",
      "&:hover": {
        backgroundColor: "#eee",
      },
    },
    [STATUS_READY]: {
      border: `3px solid ${statusLooks[STATUS_READY].color}`,
      cursor: "pointer",
      "&:hover": {
        backgroundColor: "#eee",
      },
    },
    [STATUS_UNDER_REVIEW]: {
      cursor: "pointer",
      "&:hover": {
        backgroundColor: "#eee",
      },
    },
    [STATUS_ERROR]: {
      cursor: "pointer",
      "&:hover": {
        backgroundColor: "#eee",
      },
    },
  };

  const inner = (
    <Paper withBorder p="md" sx={styles[status]}>
      <Group position="apart">
        <Group>
          <Text fz={theme.spacing.xl * 2} ml="md" mr="md">
            {index + 1}
          </Text>
          <Stack>
            <Title order={2}>{title}</Title>
            <Text>{blurb}</Text>
          </Stack>
        </Group>
        <Icon size={theme.spacing.xl * 3} color={color} />
      </Group>
    </Paper>
  );

  if (status === STATUS_BLOCKED) {
    return (
      <Tooltip label="Not so fast! You can't access this step until you have done all the previous ones">
        {inner}
      </Tooltip>
    );
  }

  return <Link href={`${router.asPath}/steps/${index}`}>{inner}</Link>;
}
