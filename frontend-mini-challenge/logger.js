import pino from "pino";

import { LOG_LEVEL, GIT_COMMIT_SHA, LOKI_HOST_URL } from "./config";

// import { GetServerSidePropsContext } from "next";

// const transport = pino.transport({
//   targets: [
//     // {
//     //   target: 'pino/file',
//     //   options: { destination: `${__dirname}/app.log` },
//     // },
//     {
//
//     },
// {
//     target: "pino-pretty",
// }
//   ],
// });

// module.exports = pino(
//   {
//     level: process.env.PINO_LOG_LEVEL || "info",
//     timestamp: pino.stdTimeFunctions.isoTime,
//   },
//   transport
// );

// pino.transport

const LokiTransport = {
  target: "pino-loki",
  options: {
    batching: true,
    interval: 5,
    silenceErrors: false,

    host: `${LOKI_HOST_URL}:3100`,
    // basicAuth: {
    //   username: "username",
    //   password: "password",
    // },
  },
};

// const LokiTransport = {
//   target: "pino-loki-transport",
//   options: {
//     lokiUrl: LOKI_HOST_URL,
//   },
// };

const customLevels = {
  http: 35, // Any number between info (30) and warn (40) will work the same
};

const logger = pino({
  level: LOG_LEVEL,
  customLevels,
  formatters: {
    //   level: (label) => {
    //     return { level: label.toUpperCase() };
    //   },
    bindings: (bindings) => {
      return {
        pid: bindings.pid,
        host: bindings.hostname,
        // node_version: process.version,
        git_commit: GIT_COMMIT_SHA,
        app: "frontend-mini-challenge",
      };
    },
  },
  // timestamp: () => `,"time":"${new Date(Date.now()).toISOString()}"`,
  transport: {
    targets: [LokiTransport],
  },
});

export default logger;

// process.on('uncaughtException', (err) => {
//     // log the exception
//     logger.fatal(err, 'uncaught exception detected');
//     // shutdown the server gracefully
//     server.close(() => {
//       process.exit(1); // then exit
//     });

//     // If a graceful shutdown is not achieved after 1 second,
//     // shut down the process completely
//     setTimeout(() => {
//       process.abort(); // exit immediately and generate a core dump file
//     }, 1000).unref()
//     process.exit(1);
//   });
