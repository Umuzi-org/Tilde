// TODO: make sure it's responsive: https://mantine.dev/core/app-shell/

import {
  AppShell,
  Header,
  Group,
  Menu,
  ActionIcon,
  Text,
  Container,
} from "@mantine/core";
import { useWhoAmI, useLogout } from "../apiHooks";
import { ProfileIcon, SettingsIcon, LogoutIcon } from "../brand";
import { useEffect } from "react";
import { useRouter } from "next/router";
import { getAuthToken } from "../lib/authTokenStorage";

export default function Page({ children }) {
  const { responseData: userData, status: whoAmIStatus } = useWhoAmI();

  const { call: callLogout, isLoading } = useLogout();
  const router = useRouter();

  useEffect(() => {
    const token = getAuthToken();

    if (!token) {
      console.log("no token. redirecting");
      router.push("/");
      return;
    }

    if (whoAmIStatus === 401) {
      console.log("WHO AM I 401. redirecting");
      router.push("/");
      return;
    }
  });

  function handleLogout() {
    callLogout();
  }

  const props = {
    whoAmIStatus,
    userData,
    handleLogout,
  };

  return <Presentation {...props}>{children}</Presentation>;
}

export function Presentation({
  whoAmIStatus,
  userData,
  handleLogout,
  children,
}) {
  const router = useRouter();
  return (
    <AppShell
      padding="md"
      header={
        <Header height={60} p="xs">
          {whoAmIStatus === 200 && (
            <Group sx={{ height: "100%" }} px={20} position="right">
              <Text>
                You are logged in as {userData.firstName || userData.email}
              </Text>
              <Menu shadow="md" width={200}>
                <Menu.Target>
                  <ActionIcon variant="light">
                    <ProfileIcon size={30} />
                  </ActionIcon>
                </Menu.Target>
                <Menu.Dropdown>
                  <Menu.Item
                    icon={<SettingsIcon size={14} />}
                    onClick={() => {
                      router.push("/settings");
                    }}
                  >
                    Settings
                  </Menu.Item>
                  <Menu.Divider />
                  <Menu.Item
                    icon={<LogoutIcon size={14} />}
                    onClick={handleLogout}
                  >
                    Log out
                  </Menu.Item>
                </Menu.Dropdown>
              </Menu>
            </Group>
          )}
        </Header>
      }
    >
      <Container style={{ minHeight: "100%" }}>{children}</Container>
    </AppShell>
  );
}
