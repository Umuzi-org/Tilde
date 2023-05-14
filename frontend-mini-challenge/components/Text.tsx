import { Text } from "@mantine/core";

export function Bold({ children }: { children: React.ReactNode }) {
  return (
    <Text fw={700} component="span">
      {children}
    </Text>
  );
}

export function Underlined({ children }: { children: React.ReactNode }) {
  return (
    <Text td="underline" component="span">
      {children}
    </Text>
  );
}
