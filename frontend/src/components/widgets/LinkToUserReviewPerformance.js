import { routes } from "../../routes";

export function getUrl({ userId }) {
  return routes.userCodeReviewPerformance.route.path.replace(":userId", userId);
}
