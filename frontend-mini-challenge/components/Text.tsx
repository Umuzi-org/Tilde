import { Text } from "@mantine/core";

export function Bold({ children }: { children: string }) {
  return (
    <Text fw={700} component="span">
      {children}
    </Text>
  );
}

export function Underlined({ children }: { children: string }) {
  return (
    <Text td="underline" component="span">
      {children}
    </Text>
  );
}
