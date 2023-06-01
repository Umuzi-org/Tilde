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
  LoadingOverlay,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import Link from "next/link";
import { usePasswordReset } from "../../apiHooks";
import { InfoAlert } from "../../components/Alerts";

export default function ForgotPassword({ loggedOutPageProps }) {
  const { call, requestData, isLoading } = usePasswordReset();

  const form = useForm({
    initialValues: {
      email: "",
    },

    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
    },
  });

  const sentTo = isLoading ? null : requestData && requestData.email;

  function handleSubmit({ email }) {
    call({ email, origin: window.location.origin });
  }

  return (
    <Page {...loggedOutPageProps}>
      <Box sx={{ maxWidth: 300 }} mx="auto">
        <Title>Forgot Password</Title>

        {sentTo && (
          <InfoAlert title="Password reset message sent">
            We sent a message to {sentTo}. Please keep an eye on your inbox. And
            your spam folder just in case.
          </InfoAlert>
        )}

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <div style={{ position: "relative" }}>
            <LoadingOverlay visible={isLoading} overlayBlur={1} />
            <TextInput
              mt="md"
              withAsterisk
              label="Email"
              placeholder="your@email.com"
              {...form.getInputProps("email")}
            />
            <Group position="center" mt="md">
              <Link href="/login">
                <Text mt="md">Back to login</Text>
              </Link>
            </Group>
            <Group position="center" mt="md">
              <Button type="submit" disabled={isLoading}>
                Reset Password
              </Button>
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
