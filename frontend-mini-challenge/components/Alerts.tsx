import { Alert } from "@mantine/core";
import { ErrorIcon, InfoIcon } from "../brand";

const ICON_SIZE = "2rem";

export function ErrorAlert({
  children,
  title,
}: {
  children: React.ReactNode;
  title?: string;
}) {
  return (
    <Alert
      icon={<ErrorIcon size={ICON_SIZE} />}
      mt="md"
      title={title || "Bummer!"}
      color="red"
      variant="outline"
    >
      {children}
    </Alert>
  );
}

export function InfoAlert({
  children,
  title,
  Icon,
}: {
  children: React.ReactNode;
  title: string;
  Icon: React.FunctionComponent<{ size: string }>;
}) {
  return (
    <Alert
      icon={<Icon size={ICON_SIZE} />}
      mt="md"
      title={title}
      color="blue"
      variant="outline"
    >
      {children}
    </Alert>
  );
}
