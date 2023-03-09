export const STATUS_DONE = "DONE";
export const STATUS_BLOCKED = "BLOCKED";
export const STATUS_READY = "READY";
// const STATUS_IN_PROGRESS = "IN_PROGRESS";

export const steps = [
  {
    title: "Setup your device",
    blurb: "Get set up to write HTML code on your own computer",
    status: STATUS_DONE,
  },
  {
    title: "Hello HTML",
    blurb:
      "HTML is a kind of programming language that lets you lay out website content",
    status: STATUS_READY,
  },
  {
    title: "Register with Github",
    blurb:
      "If you're going to be a coder, you're going to need to get Git. This is the first step",
    status: STATUS_BLOCKED,
  },
  {
    title: "Your first website",
    blurb: "You'll host your very first website :) So exciting!",
    status: STATUS_BLOCKED,
  },
  {
    title: "Feedback",
    blurb: "Let us know how it went",
    status: STATUS_BLOCKED,
  },
];
