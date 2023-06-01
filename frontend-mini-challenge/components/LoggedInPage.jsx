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
import { useLogout, serverSideWhoAmI } from "../apiHooks";
import { ProfileIcon, SettingsIcon, LogoutIcon } from "../brand";
import { useEffect } from "react";
import { useRouter } from "next/router";
import { clearAuthToken, useAuthCookies } from "../lib/authTokenStorage";
// import { useCookies } from "react-cookie";
import logger from "../logger";

const LOGOUT_REDIRECT_PAGE = "/login";

export default function Page({
  children,
  serverSidePropsCorrectlyCalled,
  isLoggedIn,
  loggedInUserData,
}) {
  if (!serverSidePropsCorrectlyCalled) {
    throw new Error(
      "It looks like you didn't make use of the getServerSideProps function defined below"
    );
  }

  const { clearCookies } = useAuthCookies();
  const { call: callLogout, status } = useLogout();
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn) {
      clearAuthToken();
      clearCookies();

      router.push(LOGOUT_REDIRECT_PAGE);
    }
  });

  useEffect(() => {
    if (status) router.push(LOGOUT_REDIRECT_PAGE);
  });

  function handleLogout() {
    callLogout();
  }

  const props = {
    handleLogout,
    loggedInUserData,
  };

  return <Presentation {...props}>{children}</Presentation>;
}

export function Presentation({ handleLogout, loggedInUserData, children }) {
  const router = useRouter();
  return (
    <AppShell
      padding="md"
      header={
        <Header height={60} p="xs">
          <Group sx={{ height: "100%" }} px={20} position="right">
            <Text>
              You are logged in as{" "}
              {loggedInUserData.firstName || loggedInUserData.email}
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
        </Header>
      }
    >
      <Container style={{ minHeight: "100%" }}>{children}</Container>
    </AppShell>
  );
}

/* NOTE: 

This wont get called automatically by next, it needs to be imported and used in the pages that make use of this component.  

How to use this:

Inside the page file create a getServerSideProps function that looks like this:

export async function getServerSideProps({ query, req }) {
  const loggedInPageProps = await getServerSidePropsForLoggedInPage({
    query,
    req,
  });

  // any other server side logic you need to run

  return {
    props: {
      loggedInPageProps,
      // ...anyOtherPropsYouCareAbout
    },
  };
}

Then when you make use of this page component:

    <Page {...loggedInPageProps}>
      {loggedInPageProps.isLoggedIn && <Presentation {...props} />}
    </Page>

*/
export async function getServerSidePropsForLoggedInPage({ query, req }) {
  const whoAmIResponse = await serverSideWhoAmI({ query, req });

  const { userId } = whoAmIResponse.responseData;
  const { url } = req;

  logger.http({ user_id: userId, url }, `Page access`);

  return {
    serverSidePropsCorrectlyCalled: true,
    isLoggedIn: whoAmIResponse.status === 200,
    // isLoggedIn: false,
    loggedInUserData: whoAmIResponse.responseData,
  };
}
