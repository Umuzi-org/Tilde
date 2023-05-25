import React from "react";
import {
  Paper,
  TableBody,
  Table,
  TableRow,
  TableCell,
  TableHead,
  Typography,
} from "@material-ui/core";
import FlavourChips from "../../widgets/FlavourChips";
// TODO: put storypoints back once Sam is finished with calcs
// import StoryPoints from "../../widgets/StoryPoints";

import { routes } from "../../../routes";
import { Link } from "react-router-dom";

import IconButton from "@material-ui/core/IconButton";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import ArrowLeftIcon from "@material-ui/icons/ArrowLeft";

import CompetenceReview from "./CompetenceReview";
import PullRequestReview from "./PullRequestReview";

import HelpIcon from "@material-ui/icons/Help";

import Modal from "../../widgets/Modal";
const COMPETENCE_REVIEW = "competence";
const PR_REVIEW = "pr";

function Presentation({
  competenceReviews,
  pullRequestReviews,
  startDate,
  endDate,
  days,

  handleClickPrevious,
  handleClickNext,

  // help modal
  showReviewHelpModal,
  handleOpenReviewHelpModal,
  handleCloseReviewHelpModal,
}) {
  competenceReviews = competenceReviews || [];
  pullRequestReviews = pullRequestReviews || [];

  const grouped = {};

  for (let review of competenceReviews) {
    const { contentItem, flavourNames, title, contentItemAgileWeight } = review;

    const key = JSON.stringify({
      contentItem,
      flavourNames,
      title,
      contentItemAgileWeight,
    });
    grouped[key] = grouped[key] || [];
    grouped[key].push({ ...review, type: COMPETENCE_REVIEW });
  }

  for (let review of pullRequestReviews) {
    const { contentItem, flavourNames, title, contentItemAgileWeight } = review;

    const key = JSON.stringify({
      contentItem,
      flavourNames,
      title,
      contentItemAgileWeight,
    });
    grouped[key] = grouped[key] || [];
    grouped[key].push({
      ...review,
      type: PR_REVIEW,
      timestamp: review.submittedAt,
    });
  }

  return (
    <React.Fragment>
      <Modal open={showReviewHelpModal} onClose={handleCloseReviewHelpModal}>
        <Paper>
          <Typography variant="h4">Reviews</Typography>
          <Typography>
            The Reviews column shows all the reviews that happened on a
            particular project during the selected time period. Each review is
            represented as a rectangle.
          </Typography>
          <Typography>
            You can hover over a review to see some basic details. Clicking on a
            review will take you to the details page of the reviewed card.
          </Typography>

          <br />
          <Typography>The color coding is explained below:</Typography>

          <br />

          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell colSpan={2}>Pull request reviews</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>
                  <PullRequestReview
                    review={{
                      id: 54897,
                      state: "changes_requested",
                      submittedAt: "2022-01-20T07:51:27Z",
                      flavourNames: ["javascript"],
                      contentItem: 225,
                      title: "Animals Part 2. Adding Tests",
                      contentItemAgileWeight: 30,
                      agileCard: 159614,
                      user: 219,
                      validated: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  If you see one of these then it means you reviewed a pull
                  request.
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <PullRequestReview
                    review={{
                      id: 54897,
                      state: "approved",
                      submittedAt: "2022-01-20T07:51:27Z",
                      flavourNames: ["javascript"],
                      contentItem: 225,
                      title: "Animals Part 2. Adding Tests",
                      contentItemAgileWeight: 30,
                      agileCard: 159614,
                      user: 219,
                      validated: "d",
                    }}
                  />
                </TableCell>
                <TableCell>
                  If you see one of these then it means you approved a PR and
                  then someone requested changes or dismissed the same PR.
                  Someone is disagreeing with you. If you see one of these then
                  try to learn from it. Go look at the recent reviews on the
                  card and see what you missed.
                  <br />
                  <br />
                  You might be able to learn something from the other reviewer.
                  Or maybe they can learn something from you.
                </TableCell>
              </TableRow>
            </TableBody>

            <TableHead>
              <TableRow>
                <TableCell colSpan={2}>Positive competence reviews</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: null,
                      agileCard: 207289,
                      status: "C",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  A perfectly normal competence review. If you see one of these
                  then it means you marked someone as competent
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: true,
                      validated: null,
                      agileCard: 207289,
                      status: "C",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  The styling on this one means that you left a trusted review.
                  If you do a good job of reviewing a certain project then
                  you'll earn trust.
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: "i",
                      agileCard: 207289,
                      status: "E",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  You marked someone as excellent and then a trusted reviewer
                  added a negative review.
                  <br />
                  <br />
                  <strong>
                    If you don't know what competent looks like then you need to
                    work on that.
                  </strong>{" "}
                  If you see one of these then try to learn from it. Go look at
                  the recent reviews on the card and see what you missed.
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: "d",
                      agileCard: 207289,
                      status: "C",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  You marked someone as competent and then a non-trusted
                  reviewer added a negative review. If you see one of these then
                  try to learn from it. Go look at the recent reviews on the
                  card and see what you missed.
                  <br />
                  <br />
                  You might be able to learn something from the other reviewer.
                  Or maybe they can learn something from you.
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: "c",
                      agileCard: 207289,
                      status: "E",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  You added a positive review and then a trusted reviewer closed
                  the card. That means you were right.
                </TableCell>
              </TableRow>
            </TableBody>
            <TableHead>
              <TableRow>
                <TableCell colSpan={2}>Negative competence reviews</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: null,
                      agileCard: 207289,
                      status: "N",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: null,
                    }}
                  />
                </TableCell>
                <TableCell>
                  A perfectly normal competence review. If you see one of these
                  then it means you marked someone as not yet competent
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: null,
                      agileCard: 207289,
                      status: "N",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: false,
                    }}
                  />
                </TableCell>
                <TableCell>
                  You gave feedback to someone and then they asked for another
                  review and they got more feedback. That means one of two
                  things: Either the feedback you gave was insufficient in some
                  way; or the person you reviewed did not implement the feedback
                  properly. This is BAD!
                  <br />
                  <br /> If you give someone feedback then you must always try
                  to set them up to succeed. Your feedback must:
                  <ul>
                    <li>
                      Make sense - write clearly and make use of markdown syntax
                      to add meaning
                    </li>
                    <li>
                      Point out all the problems you find, be thorough and
                      informative
                    </li>
                  </ul>
                  If you see one of these then try to learn from it: <br /> Go
                  look at the recent reviews on the card and see what you missed
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell>
                  <CompetenceReview
                    review={{
                      id: 48678,
                      flavourNames: [],
                      contentItem: 316,
                      title: "FreeCodeCamp - Basic Javascript",
                      trusted: false,
                      validated: null,
                      agileCard: 207289,
                      status: "N",
                      timestamp: "2022-09-13T08:52:56.187979Z",
                      reviewerUser: 219,
                      contentItemAgileWeight: 12,
                      completeReviewCycle: true,
                    }}
                  />
                </TableCell>
                <TableCell>
                  You gave feedback to someone and then they asked for another
                  review and then they got marked as competent. That means that
                  they had enough feedback to succeed. This is AWESOME! Always
                  remember that feedback is a gift, you helped set someone up
                  for success by telling them what they needed to hear.{" "}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </Paper>
      </Modal>
      <Paper>
        <IconButton aria-label="previous" onClick={handleClickPrevious}>
          <ArrowLeftIcon />
        </IconButton>
        {new Intl.DateTimeFormat().format(startDate)} -
        {new Intl.DateTimeFormat().format(endDate)} ({days} days)
        <IconButton aria-label="next" onClick={handleClickNext}>
          <ArrowRightIcon />
        </IconButton>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Project</TableCell>
              <TableCell>
                Competence review count <br />
                total: {competenceReviews.length}
              </TableCell>
              <TableCell>
                PR review count <br /> total: {pullRequestReviews.length}
              </TableCell>
              <TableCell>
                Reviews{" "}
                <IconButton onClick={handleOpenReviewHelpModal}>
                  <HelpIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(grouped)
              .sort((a, b) => {
                const weightA = JSON.parse(a).contentItemAgileWeight;
                const weightB = JSON.parse(b).contentItemAgileWeight;
                return weightB - weightA;
              })
              .map((key) => {
                const {
                  // contentItem,
                  flavourNames,
                  title,
                  // contentItemAgileWeight, // TODO: put storypoints back once Sam is finished with calcs
                } = JSON.parse(key);
                const reviews = grouped[key];
                return (
                  <TableRow key={key}>
                    <TableCell>
                      {title}
                      <br />
                      <FlavourChips
                        flavourNames={flavourNames}
                        variant="small"
                      />
                      {/* <StoryPoints // TODO: put storypoints back once Sam is finished with calcs
                      storyPoints={contentItemAgileWeight}
                      variant="small"
                    /> */}
                    </TableCell>
                    <TableCell>
                      {
                        reviews.filter((r) => r.type === COMPETENCE_REVIEW)
                          .length
                      }
                    </TableCell>
                    <TableCell>
                      {reviews.filter((r) => r.type === PR_REVIEW).length}
                    </TableCell>
                    <TableCell>
                      {reviews
                        .sort(
                          (a, b) =>
                            new Date(a.timestamp) - new Date(b.timestamp)
                        )
                        .map((review) => (
                          <Link
                            to={routes.cardDetails.route.path.replace(
                              ":cardId",
                              review.agileCard
                            )}
                          >
                            {review.type === COMPETENCE_REVIEW && (
                              <CompetenceReview review={review} />
                            )}

                            {review.type === PR_REVIEW && (
                              <PullRequestReview review={review} />
                            )}
                          </Link>
                        ))}
                    </TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </Paper>
    </React.Fragment>
  );
}

export default Presentation;
