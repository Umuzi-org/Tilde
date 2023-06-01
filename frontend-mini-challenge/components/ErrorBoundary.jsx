import React from "react";
import { Presentation } from "./LoggedOutPage";

import logger from "../logger";

import { Title, Text, Stack } from "@mantine/core";
import Link from "next/link";

function ErrorBoundaryFallback() {
  return (
    <Presentation>
      <Stack spacing="md">
        <Title order={1}>Oops, there was an error!</Title>
        <Text>
          Something went wrong! We are aware ofd the problem and are working on
          sorting it all out.
        </Text>

        <Text>
          <Link href="/">Go to Home page</Link>
        </Text>
      </Stack>
    </Presentation>
  );
}

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    // Define a state variable to track whether is an error or not
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.log({ error, errorInfo }, "componentDidCatch console");
    logger.info({ error, errorInfo }, "componentDidCatch info");
    logger.error({ error, errorInfo }, "componentDidCatch error");
    logger.error({ error, errorInfo }, "Uncaught client-side error");
  }

  render() {
    // Check if the error is thrown
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return <ErrorBoundaryFallback />;
    }

    // Return children components in case of no error

    return this.props.children;
  }
}

export default ErrorBoundary;
