import Page, {
  getServerSidePropsForLoggedInPage,
} from "../../components/LoggedInPage";
import {
  Title,
  Button,
  Group,
  Box,
  PasswordInput,
  Breadcrumbs,
  LoadingOverlay,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import Link from "next/link";
import { useRouter } from "next/router";
import { useChangePassword } from "../../apiHooks";
import { ErrorAlert, InfoAlert } from "../../components/Alerts";

export default function Settings({ loggedInPageProps }) {
  const router = useRouter();
  const { call, isLoading, status, responseData } = useChangePassword();

  const form = useForm({
    initialValues: {
      oldPassword: "",
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

  function goBack(e) {
    e.preventDefault();
    router.back();
  }

  function handleSubmit({ newPassword1, newPassword2, oldPassword }) {
    call({ newPassword1, newPassword2, oldPassword });
  }

  const formErrors = {};

  if (status) {
    Object.keys(responseData).forEach((key) => {
      formErrors[key] = { error: responseData[key] };
    });
  }

  return (
    <Page {...loggedInPageProps}>
      <Breadcrumbs>
        <Link onClick={goBack} href="">
          Back
        </Link>
      </Breadcrumbs>
      <Box sx={{ maxWidth: 300 }} mx="auto">
        <Title>Change Password</Title>
        {status === 400 && (
          <ErrorAlert>
            Something went wrong. See form field errors below
          </ErrorAlert>
        )}
        {status === 200 && (
          <InfoAlert title={"Success"}>
            Your password has been updated
          </InfoAlert>
        )}
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <div style={{ position: "relative" }}>
            <LoadingOverlay visible={isLoading} overlayBlur={1} />

            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="Old password"
              {...form.getInputProps("oldPassword")}
              {...formErrors.oldPassword}
              autoComplete="password"
            />

            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="New password"
              {...form.getInputProps("newPassword1")}
              {...formErrors.newPassword1}
              autoComplete="new-password"
            />

            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="Confirm password"
              {...form.getInputProps("newPassword2")}
              {...formErrors.newPassword2}
              autoComplete="new-password"
            />

            <Group position="center" mt="md">
              <Button type="submit">Save Password</Button>
            </Group>
          </div>
        </form>
      </Box>
    </Page>
  );
}

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
