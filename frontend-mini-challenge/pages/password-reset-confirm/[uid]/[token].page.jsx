import Page, {
  getServerSidePropsForLoggedOutPage,
} from "../../../components/LoggedOutPage";
import {
  Title,
  Button,
  Group,
  Box,
  PasswordInput,
  LoadingOverlay,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useRouter } from "next/router";
import { useEffect } from "react";
import { useConfirmPasswordReset } from "../../../apiHooks";
import { ErrorAlert } from "../../../components/Alerts";

export default function ResetPassword({ loggedOutPageProps }) {
  const router = useRouter();
  const form = useForm({
    initialValues: {
      newPassword1: "",
      newPassword2: "",
    },

    validate: {
      newPassword1: (value) =>
        value.length < 8 ? "Password must be at least 8 characters" : null,
      newPassword2: (value, { newPassword1 }) =>
        value === newPassword1 ? null : "Passwords do not match",
    },
  });

  const { call, status, isLoading, responseData } = useConfirmPasswordReset();

  useEffect(() => {
    if (status === 200) router.push("/password-reset-complete");
    // TODO: Toast: The password has been reset with the new password. Or redurect do a "page that just says "complete"
  }, [router, status]);

  function handleSubmit({ newPassword1, newPassword2 }) {
    const { token, uid } = router.query;
    call({ newPassword1, newPassword2, token, uid });
  }

  return (
    <Page {...loggedOutPageProps}>
      <Box sx={{ maxWidth: 300 }} mx="auto">
        <Title>Reset Password</Title>
        {status === 400 && (
          <ErrorAlert>
            {responseData.token || responseData.uid
              ? "This password reset link is invalid. Have you already used it? When you attempt to reset your password then it is important that you follow the password reset link in the latest email you received."
              : Object.values(responseData)}
          </ErrorAlert>
        )}

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <div style={{ position: "relative" }}>
            <LoadingOverlay
              visible={isLoading}
              overlayBlur={1}
              // loaderProps={{ size: "xl" }}
            />
            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="New password"
              {...form.getInputProps("newPassword1")}
            />

            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="Confirm password"
              {...form.getInputProps("newPassword2")}
            />

            <Group position="center" mt="md">
              <Button type="submit">Confirm</Button>
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
