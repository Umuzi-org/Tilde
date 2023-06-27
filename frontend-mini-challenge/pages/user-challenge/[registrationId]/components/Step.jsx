import {
  Paper,
  Stack,
  Text,
  Title,
  useMantineTheme,
  Tooltip,
  Group,
  LoadingOverlay,
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
import { useState } from "react";

export default function Step({ index, title, blurb, status }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const theme = useMantineTheme();
  const { Icon, color } = statusLooks[status];

  const clickableStyle = {
    cursor: "pointer",
    "&:hover": {
      backgroundColor: "#eee",
    },
  };
  const styles = {
    [STATUS_BLOCKED]: {
      cursor: "not-allowed",
    },
    [STATUS_DONE]: {
      ...clickableStyle,
    },
    [STATUS_READY]: {
      border: `3px solid ${statusLooks[STATUS_READY].color}`,
      ...clickableStyle,
    },
    [STATUS_UNDER_REVIEW]: {
      ...clickableStyle,
    },
    [STATUS_ERROR]: {
      border: `3px solid ${statusLooks[STATUS_ERROR].color}`,
      ...clickableStyle,
    },
  };

  const inner = (
    <div style={{ position: "relative" }}>
      <LoadingOverlay visible={loading} overlayBlur={1} />

      <Paper withBorder p="md" sx={styles[status]}>
        <Stack align="flex-start">
          <Group>
            <Icon size={"3rem"} color={color} />
            <Title order={2}>
              Step {index + 1} - {title}
            </Title>
          </Group>
          <Text>{blurb}</Text>
        </Stack>
      </Paper>
    </div>
  );

  if (status === STATUS_BLOCKED) {
    return (
      <Tooltip label="Not so fast! You can't access this step until you have done all the previous ones">
        {inner}
      </Tooltip>
    );
  }

  return (
    <Link
      onClick={() => setLoading(true)}
      href={`${router.asPath}/steps/${index}`}
    >
      {inner}
    </Link>
  );
}
