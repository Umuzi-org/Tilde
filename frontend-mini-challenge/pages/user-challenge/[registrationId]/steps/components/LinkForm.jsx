import {
  Title,
  Button,
  Box,
  TextInput,
  Group,
  LoadingOverlay,
} from "@mantine/core";

import { ErrorAlert, InfoAlert } from "../../../../../components/Alerts";
import { useForm } from "@mantine/form";

export default function LinkForm({
  linkExample,
  linkName,
  handleSubmit,
  status,
  responseData,
  linkSubmission,
  isLoading,
}) {
  const form = useForm({
    initialValues: {
      linkSubmission: linkSubmission || "",
    },

    validate: {
      linkSubmission: (value) =>
        value && value.startsWith("https://")
          ? null
          : "Please fill in a valid url",
    },
  });
  const formErrors = {};

  if (status === 400) {
    Object.keys(responseData).forEach((key) => {
      formErrors[key] = { error: responseData[key] };
    });
  }

  return (
    <Box sx={{ maxWidth: 300 }} mx="auto" mt="md">
      <Title order={3}>Project submission</Title>
      {status === 400 && (
        <ErrorAlert>
          {responseData.nonFieldErrors || "Please correct the errors below"}
        </ErrorAlert>
      )}
      {status === 200 && (
        <InfoAlert title={"Success"}>
          Your project link has been submitted for review{" "}
        </InfoAlert>
      )}
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <div style={{ position: "relative" }}>
          <LoadingOverlay visible={isLoading} overlayBlur={1} />
          <TextInput
            mt="md"
            withAsterisk
            placeholder={linkExample}
            label={linkName}
            {...form.getInputProps("linkSubmission")}
            {...formErrors.linkSubmission}
          />
          <Group position="right" mt="md">
            <Button type="submit" variant={"outline"}>
              Update and submit for review
            </Button>
          </Group>
        </div>
      </form>
    </Box>
  );
}
