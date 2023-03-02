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

export default function ChangePassword() {
  const form = useForm({
    initialValues: {
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
    },

    validate: {
      newPassword: (value) =>
        value.length < 8 ? "Password must be at least 8 characters" : null,
      confirmPassword: (value, { password }) =>
        value === password ? null : "Passwords do not match",
    },
  });
  return (
    <Page>
      <Container>
        <Box sx={{ maxWidth: 300 }} mx="auto">
          <Title>Change Password</Title>
          <form onSubmit={form.onSubmit((values) => console.log(values))}>
            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="Old password"
              {...form.getInputProps("oldPassword")}
            />

            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="New password"
              {...form.getInputProps("newPassword")}
            />

            <PasswordInput
              mt="md"
              withAsterisk
              placeholder="Password"
              label="Confirm password"
              {...form.getInputProps("confirmPassword")}
            />

            <Group position="center" mt="md">
              <Button type="submit">Save</Button>
            </Group>
          </form>
        </Box>
      </Container>{" "}
    </Page>
  );
}
