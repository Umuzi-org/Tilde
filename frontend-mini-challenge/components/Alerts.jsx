import { Alert } from "@mantine/core";
import { ErrorIcon, InfoIcon } from "../brand";

export function ErrorAlert({ children, title }) {
  return (
    <Alert
      icon={<ErrorIcon size={16} />}
      mt="md"
      title={title || "Bummer!"}
      color="red"
      variant="outline"
    >
      {children}
    </Alert>
  );
}

export function InfoAlert({ children, title }) {
  return (
    <Alert
      icon={<InfoIcon size={16} />}
      mt="md"
      title={title}
      color="blue"
      variant="outline"
    >
      {children}
    </Alert>
  );
}
