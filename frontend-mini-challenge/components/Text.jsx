import { Text } from "@mantine/core";

export function Bold({ children }) {
  return (
    <Text fw={700} component="span">
      {children}
    </Text>
  );
}

export function Underlined({ children }) {
  return (
    <Text td="underline" component="span">
      {children}
    </Text>
  );
}
