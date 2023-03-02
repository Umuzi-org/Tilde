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

export default function Login() {
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
  return (
    <Page>
      <Container>
        <Box sx={{ maxWidth: 300 }} mx="auto">
          <Title>Login</Title>
          <form onSubmit={form.onSubmit((values) => console.log(values))}>
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
          </form>
        </Box>
      </Container>{" "}
    </Page>
  );
}
