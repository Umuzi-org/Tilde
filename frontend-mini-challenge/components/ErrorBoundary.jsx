import React from "react";
import { Presentation } from "./LoggedOutPage";

import { forceLog } from "../logger";

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
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ ...this.state, error, errorInfo });
    forceLog({ level: 60, message: errorInfo.componentStack });
  }

  render() {
    // Check if the error is thrown
    if (this.state.hasError) {
      return <ErrorBoundaryFallback />;
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
