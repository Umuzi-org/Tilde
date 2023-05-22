import { Alert } from "@mantine/core";
import { ErrorIcon, InfoIcon } from "../brand";

const ICON_SIZE = "2rem";


interface Props {
  title: string;
  children: string;
}

export function ErrorAlert({ children, title }: Props) {
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

export function InfoAlert({ children, title }: Props) {
  return (
    <Alert
      icon={<InfoIcon size={ICON_SIZE} />}
      mt="md"
      title={title}
      color="blue"
      variant="outline"
    >
      {children}
    </Alert>
  );
}

