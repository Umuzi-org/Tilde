import { Center, Container, Stack, Text, Title } from "@mantine/core";
import Link from "next/link";
import logger from "../logger";
import { useRouter } from "next/router";
import { useEffect } from "react";

export default function ErrorPage() {
  const router = useRouter();

  useEffect(() => {
    // TODO: for some reason this logs twice. It needs to log once instead
    logger.warn({ user_id: null, url: router.asPath }, `Page Access 404`);
  }, [router.asPath]);

  return (
    <Center mah={"100%"} mx="auto" my="25%">
      <Stack spacing="md" align="center">
        <Title order={1}>404</Title>
        <Text>This page does not exist!</Text>
        <Text>
          <Link href={"/"}>Go Home</Link>
        </Text>
      </Stack>
    </Center>
  );
}

// export const getStaticProps = async () => {
//   return { props: {} };
// };
