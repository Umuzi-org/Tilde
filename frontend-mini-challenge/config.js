export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export const REST_AUTH_BASE_URL = `${API_BASE_URL}/api/dj-rest-auth`;

export const DISCORD_SERVER_URL =
  process.env.NEXT_PUBLIC_DISCORD_SERVER_URL || "https://discord.gg/fKmUsZpmwC"; // TODO: Get from settings
