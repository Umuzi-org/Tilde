import { LOKI_HOST_URL } from "../../../../../config";
import { LOG_LEVELS } from "../../../../../logger";

export default async function handler(req, res) {
  const streams = req.body.streams.map((stream) => {
    const { values } = stream;
    console.log({ values });
    return {
      stream: {
        ...stream.stream,
        level: Object.keys(LOG_LEVELS)
          .find((key) => LOG_LEVELS[key] === stream.stream.level)
          .toUpperCase(),
      },
      values: stream.values.map((value) => {
        const final = JSON.parse(value[1]);
        delete final.stack_trace; // rather than deleting it, shorten it
        return [value[0], JSON.stringify(final)];
      }),
    };
  });

  const response = await fetch(`${LOKI_HOST_URL}:3100/loki/api/v1/push`, {
    method: "POST",
    body: JSON.stringify({ streams }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  const { status } = response;
  const text = await response.text();

  // console.log({ status, text });
  res.status(status).json(text);
  // res.status(200).json({ message: "Hello from Next.js!" });
}

// async function loki_log() {
//   return await fetch(`${LOKI_HOST_URL}:3100/loki/api/v1/push`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       streams: [
//         {
//           stream: { level: "info", here: "is", some: "data" },
//           values: [
//             [
//               `${1000000 * new Date().getTime()}`,
//               "This is the message we want",
//             ],
//           ],
//         },
//       ],
//     }),
//   });
// }
