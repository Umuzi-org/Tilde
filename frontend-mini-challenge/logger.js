import pino from "pino";

import { LOG_LEVEL, GIT_COMMIT_SHA, LOKI_HOST_URL } from "./config";

const LokiTransport = {
  target: "pino-loki",
  options: {
    batching: true,
    interval: 5,
    silenceErrors: false,
    host: "http://localhost:3002/api",
    labels: {
      git_commit: GIT_COMMIT_SHA,
      app: "frontend-mini-challenge",
    },
    propsToLabels: ["level", "stack_trace"],
  },
};

// https://datatracker.ietf.org/doc/html/rfc5424#page-10
export const LOG_LEVELS = {
  emerg: 80,
  alert: 70,
  crit: 60,
  error: 50,
  warn: 40,
  notice: 30,
  http: 35, //TODO: remove
  info: 20,
  debug: 10,
};

const logger = pino({
  customLevels: LOG_LEVELS,
  useOnlyCustomLevels: true,
  formatters: {
    // level: (label) => {
    //   return { level: label.toUpperCase() };
    // },
    bindings: (bindings) => {
      return {
        host: bindings.hostname,
        timestamp: pino.stdTimeFunctions.isoTime,
      };
    },
  },
  transport: {
    targets: [
      LokiTransport,
      {
        target: "pino/file",
      },
    ],
  },
});

export default logger;

export async function forceLog({ level, message }) {
  const resp = await fetch(`http://localhost:3002/api/loki/api/v1/push`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      streams: [
        {
          stream: { level: level, here: "is", some: "data" },
          values: [[`${1000000 * new Date().getTime()}`, message]],
        },
      ],
    }),
  });

  // console.log(await resp.text());
}

// export const LOG_LEVELS = {
//   ...customLevels,
//   debug: 20,
//   info: 30,
//   warning: 40,
//   error: 50,
//   critical: 60,
// };
