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
import { useLogout, serverSideWhoAmI, TOKEN_COOKIE } from "../apiHooks";
import { ProfileIcon, SettingsIcon, LogoutIcon } from "../brand";
import { useEffect } from "react";
import { useRouter } from "next/router";
import { clearAuthToken } from "../lib/authTokenStorage";
import { useCookies } from "react-cookie";
import { GetServerSidePropsContext } from 'next';

export default function Page({
  children,
  serverSidePropsCorrectlyCalled,
  isLoggedIn,
  loggedInUserData,
}: {
  children: React.ReactNode;
  serverSidePropsCorrectlyCalled: boolean;
  isLoggedIn: boolean;
  loggedInUserData: { firstName: string; email: string }
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

export function Presentation({
  handleLogout,
  loggedInUserData,
  children,
}: {
  handleLogout: () => void;
  loggedInUserData: { firstName: string; email: string }
  children: React.ReactNode;
}) {
  const router = useRouter();
  return (
    <AppShell
      padding="md"
      header={
        <Header height={60} p="xs">
          <Group sx={{ height: "100%" }} px={20} position="right">
            <Text>
              You are logged in as {" "}
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


export const getServerSidePropsForLoggedInPage = async (context: GetServerSidePropsContext) => {
  const { req } = context;

  const whoAmIResponse = await serverSideWhoAmI({ req });

  return {
    serverSidePropsCorrectlyCalled: true,
    isLoggedIn: whoAmIResponse.status === 200,
    // isLoggedIn: false,
    loggedInUserData: whoAmIResponse.responseData,
  };
}