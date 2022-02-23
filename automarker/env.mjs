import { resolve } from "path";

export const CLONE_PATH =
  process.env.CLONE_PATH || "../gitignore/automark_clone_path";
export const PORT = process.env.AUTO_MARKER_PORT || 1313;

export const CONFIGURATION_REPO_PATH =
  process.env.CONFIGURATION_REPO_PATH || resolve("../../acn-automarker-config");
