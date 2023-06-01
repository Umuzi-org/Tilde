export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export const REST_AUTH_BASE_URL = `${API_BASE_URL}/api/dj-rest-auth`;

export const LOG_LEVEL = process.env.NEXT_PUBLIC_LOG_LEVEL || "debug";

export const GIT_COMMIT_SHA =
  process.env.NEXT_PUBLIC_GIT_COMMIT_SHA || "unknown";

export const LOKI_HOST_URL =
  process.env.NEXT_LOKI_HOST_URL || "http://localhost";
