import {
  Paper,
  Stack,
  Text,
  Title,
  useMantineTheme,
  Group,
} from "@mantine/core";

import { statusLooks } from "../../../../brand";

export default function Step({ number, title, blurb, status }) {
  const theme = useMantineTheme();
  const { Icon, color } = statusLooks[status];

  return (
    <Paper withBorder p="md">
      <Group position="apart">
        <Group>
          <Text fz={theme.spacing.xl * 2} ml="md" mr="md">
            {number}
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
}
