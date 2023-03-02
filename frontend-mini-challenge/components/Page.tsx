import { AppShell, Header } from "@mantine/core";

export default function Page({ children }) {
  return (
    <AppShell
      padding="md"
      header={
        <Header height={60} p="xs">
          {/* Header content */}
          Hey there
        </Header>
      }
    >
      {children}
    </AppShell>
  );
}
