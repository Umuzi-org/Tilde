// TODO: make sure it's responsive: https://mantine.dev/core/app-shell/

import {
  AppShell,
  Header,
  Group,
  Menu,
  ActionIcon,
  Text,
  Container,
  Affix,
  rem,
  Button,
  Tooltip,
} from "@mantine/core";
import { useLogout, serverSideWhoAmI, TOKEN_COOKIE } from "../apiHooks";
import { ProfileIcon, SettingsIcon, LogoutIcon, DiscordIcon } from "../brand";
import { useEffect } from "react";
import { useRouter } from "next/router";
import { clearAuthToken } from "../lib/authTokenStorage";
import { useCookies } from "react-cookie";
import { DISCORD_SERVER_URL } from "../config";

const LogRocket = require("logrocket");

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
  const [cookie, setCookie, removeCookie] = useCookies([TOKEN_COOKIE]);
  const { call: callLogout } = useLogout();
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn) {
      clearAuthToken();
      removeCookie(TOKEN_COOKIE, {
        path: "/",
      });

      router.push("/");
    }
  });

  useEffect(() => {
    LogRocket.identify(loggedInUserData.userId, {
      name: loggedInUserData.firstName,
      email: loggedInUserData.email,
    });
  }, [loggedInUserData]);

  function handleLogout() {
    callLogout();
    router.push("/");
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

      <Affix position={{ bottom: rem(15), right: rem(20) }}>
        <Tooltip label="Discord is a great place to chat with other people doing this challenge">
          <Button
            component="a"
            target="_blank"
            rel="noopener noreferrer"
            href={DISCORD_SERVER_URL}
            leftIcon={<DiscordIcon size={rem(20)} />}
            styles={(theme) => ({
              root: {
                backgroundColor: "rgb(88, 101, 242)",
                border: 0,
                height: rem(42),
                paddingLeft: rem(20),
                paddingRight: rem(20),
                // "&:not([data-disabled])": theme.fn.hover({
                //   backgroundColor: theme.fn.darken("#00acee", 0.05),
                // }),
              },

              leftIcon: {
                marginRight: theme.spacing.md,
              },
            })}
          >
            Join Discord Community
          </Button>
        </Tooltip>
      </Affix>
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

  return {
    serverSidePropsCorrectlyCalled: true,
    isLoggedIn: whoAmIResponse.status === 200,
    // isLoggedIn: false,
    loggedInUserData: whoAmIResponse.responseData,
  };
}
