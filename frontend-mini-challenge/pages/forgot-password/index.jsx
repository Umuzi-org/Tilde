import Page from "../../components/Page";
import {
  Container,
  Title,
  TextInput,
  Button,
  Text,
  Group,
  Box,
  PasswordInput,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import Link from "next/link";

export default function ForgotPassword() {
  const form = useForm({
    initialValues: {
      email: "",
    },

    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
    },
  });
  return (
    <Page>
      <Container>
        <Box sx={{ maxWidth: 300 }} mx="auto">
          <Title>Forgot Password</Title>
          <form onSubmit={form.onSubmit((values) => console.log(values))}>
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
              <Button type="submit">Reset Password</Button>
            </Group>
          </form>
        </Box>
      </Container>{" "}
    </Page>
  );
}
