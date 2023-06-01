import Page, {
  getServerSidePropsForLoggedOutPage,
} from "../../components/LoggedOutPage";
import {
  Title,
  TextInput,
  Button,
  Text,
  Group,
  Box,
  PasswordInput,
  LoadingOverlay,
} from "@mantine/core";

import { useForm } from "@mantine/form";
import Link from "next/link";
import { useLogin } from "../../apiHooks";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";

import { ErrorAlert } from "../../components/Alerts";

export default function Login({ loggedOutPageProps }) {
  const router = useRouter();
  const form = useForm({
    initialValues: {
      email: "",
      password: "",
    },

    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
      password: (value) => (value.length > 0 ? null : "Password is required"),
    },
  });

  const login = useLogin();
  const { call, isLoading, status, responseData } = login;

  const [calledPush, setCalledPush] = useState(false);

  useEffect(() => {
    function routerPushOnce(path) {
      if (calledPush) return;
      setCalledPush(true);
      router.push(path);
    }

    if (status === 200) routerPushOnce("/");
  }, [router, status, calledPush, setCalledPush]);

  function handleSubmit({ email, password }) {
    call({ email, password });
  }

  // throw new Error("TODO: implement this page");

  return (
    <Page {...loggedOutPageProps}>
      <Box sx={{ maxWidth: 300 }} mx="auto">
        <Title>Login</Title>

        {status === 400 && (
          <ErrorAlert>{responseData.nonFieldErrors}</ErrorAlert>
        )}
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <div style={{ position: "relative" }}>
            <LoadingOverlay
              visible={isLoading}
              overlayBlur={1}
              // loaderProps={{ size: "xl" }}
            />
            <TextInput
              mt="md"
              withAsterisk
              label="Email"
              placeholder="your@email.com"
              {...form.getInputProps("email")}
            />
            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="Password"
              {...form.getInputProps("password")}
              //   description="Password must include at least one letter, number and special character"
            />
            <Group position="center" mt="md">
              <Link href="/forgot-password">
                <Text mt="md">Forgot password?</Text>
              </Link>
            </Group>
            <Group position="center" mt="md">
              <Button type="submit">Login</Button>
            </Group>
          </div>
        </form>
      </Box>
    </Page>
  );
}

export async function getServerSideProps({ req }) {
  const loggedOutPageProps = await getServerSidePropsForLoggedOutPage({ req });

  return {
    props: {
      loggedOutPageProps,
    },
  };
}
