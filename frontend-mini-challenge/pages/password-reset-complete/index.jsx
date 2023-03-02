import { Container, Title, Text, Group } from "@mantine/core";
import Page from "../../components/LoggedOutPage";
import Link from "next/link";

export default function PasswordResetComplete() {
  return (
    <Page>
      <Container>
        <Title>Password reset successful</Title>
        <Text mt="md">
          You will now be able to login with your new password
        </Text>

        <Group position="center" mt="md">
          <Link href="/login">
            <Text mt="md">Back to Login page</Text>
          </Link>
        </Group>
      </Container>
    </Page>
  );
}
