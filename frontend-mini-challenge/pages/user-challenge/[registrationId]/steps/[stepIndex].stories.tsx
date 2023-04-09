import React from "react";
import { ComponentStory, ComponentMeta } from "@storybook/react";
import {
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_READY,
  STATUS_ERROR,
  STATUS_UNDER_REVIEW,
} from "../../../../constants";

// import { Presentation } from "./[stepIndex]";
import Presentation from "./[stepIndex].presentation";

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Presentation,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {},
} as ComponentMeta<typeof Presentation>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template: ComponentStory<typeof Presentation> = (args) => {
  return <Presentation {...args} />;
};

const registration = {
  id: 6,
  user: 3,
  curriculum: 90,
  registrationDate: "2023-03-20",
  blurb:
    "In this challenge you'll learn the basics of web development and host your first website! We'll show you how to do it, step by step. You'll also learn about some of the best FREE learning resources around so you can continue learning on your own.",
  steps: [
    {
      title: "Why learn web development?",
      blurb:
        "There are lots of different kinds of coding and non-coding careers. We'd like to show you why we're focusing on web dev and why it's probably worth your while to do take on this challenge",
      status: "DONE",
    },
    {
      title: "What is HTML?",
      blurb:
        "Web dev is cool because you don't need to be a super expert in any part of it in order to start making stuff. In this section you'll learn just enough HTML that you can start writing basic websites with simple content",
      status: "DONE",
    },
    {
      title: "How to get setup to author web code on your own device",
      blurb:
        "Every profession has it's tools: carpenters use hammers, mechanics use spanners, painters use paintbrushes.  Coders have tools too. Here you'll learn about one of the major tools of the trade.",
      status: "DONE",
    },
    {
      title: "Your first HTML page",
      blurb:
        "Time to flex your skills! In this step you'll be writing a web page from scratch on your own device.",
      status: "DONE",
    },
    {
      title: "Hosting your website on the web",
      blurb:
        "This section will be downright empowering. Once you have done this you'll be able to make websites and share them on the internet whenever you want, for free,  forever. Feel the power!",
      status: "REVIEWING",
    },
    {
      title: "Adding images to your website",
      blurb:
        "They say a picture is worth a thousand words. In this section you'll learn about how to add images to your website",
      status: "BLOCKED",
    },
    {
      title: "Adding more pages",
      blurb:
        "One of HTML's superpowers is linking. One HTML page is nice and all, but more is better.",
      status: "BLOCKED",
    },
    {
      title: "Introducing CSS",
      blurb:
        "HTML is all about the layout of your web content. CSS is all about style! In this section you'll get to add a bit of visual flair to your site",
      status: "BLOCKED",
    },
    {
      title: "Continue learning",
      blurb:
        "There are lots and lots of different kinds of coding. Web development is a great way to start off but it's really not for everyone. In this section you'll learn about a few different career paths and we'll point you at some free and awesome learning resources so you can take yourself to the next level",
      status: "BLOCKED",
    },
    {
      title: "How did we do?",
      blurb:
        "We humbly request a bit of feedback. Our goal here is to help as many people as possible. If you tell us about your experience - the good parts and the bad parts - then we'll be able to improve and help even more people. We'd really appreciate it if you filled in the survey in this step. ",
      status: "BLOCKED",
    },
  ],
  name: "Build your own website and host it on the web!",
};

const contentHtml =
  "<p>Here is a great tutorial all about HTML. Do all the sections up to the end of HTML Paragraphs.</p>\n<p>https://www.w3schools.com/html/html_intro.asp</p>\n<h2>Check your understanding before moving forward:</h2>\n<p>Understanding is critical for coders. Before you move forward, it's important that you understand a few things. Can you answer the following questions for yourself?</p>\n<ul>\n<li>What is the purpose of HTML?</li>\n<li>What is an HTML element?</li>\n<li>What is an attribute?</li>\n<li>What is the difference between <code>&#x3C;h1></code> and <code>&#x3C;h2></code>? What do these represent?</li>\n<li>How do you make a paragraph? What happens if you put 2 paragraphs underneath each other? (You can write some code yourself to check yourself)</li>\n<li>Where must the document type declaration be?</li>\n<li>What is a tag?</li>\n<li>What is the difference between an opening tag and a closing tag?</li>\n<li>How do you make use of opening and closing tags?</li>\n</ul>\n<p>If you are unsure of anything then go back to the tutorial, or spend some time on Google.</p>\n<h2>Your mission</h2>\n<p>Your mission is to make a website of your very own. It will just be one page for now.</p>\n<p>It's very important that you follow the instructions exactly, in the next step you will be deploying your website to the web.  It will need to do exactly the right thing!</p>\n<h3>1. Create a new html file called <code>index.html</code></h3>\n<p>It is important to name the file exactly right! We'll be putting it on the internet in the next step.</p>\n<h3>2. Let's make some content</h3>\n<p>This website can be about anything you want. If you like cats it can be about cats, if you like books then make it about books. Write some html code that meets the following requirements:</p>\n<ul>\n<li>it must be valid and clean html\n<ul>\n<li>the document type declaration must be correct</li>\n<li>you should be making use of valid tags</li>\n<li>any tag you open should get closed</li>\n</ul>\n</li>\n<li>it needs to have ONLY ONE <code>&#x3C;h1></code> heading</li>\n<li>it needs to make use of <code>&#x3C;h2></code> headings</li>\n<li>it needs to make use of paragraphs</li>\n<li>there should be no text that is sitting outside of a heading or paragraph element.</li>\n</ul>\n<h3>That's it</h3>\n<p>Make sure your website works on your own device. In the next step we'll get it online!</p>\n";

export const TopicBlocked = Template.bind({});
TopicBlocked.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 3,
  registration,
  stepDetails: {
    contentType: "T",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/your-first-html-page/_index.md",
    projectSubmissionType: null,
    linkName: null,
    linkExample: null,
    linkMessage: null,
    linkSubmission: null,
    reviews: [],
    title: "Your first HTML page",
    status: STATUS_BLOCKED,
    blurb:
      "Time to flex your skills! In this step you'll be writing a web page from scratch on your own device.",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/3",
};

export const TopicReady = Template.bind({});
TopicReady.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 3,
  registration,
  stepDetails: {
    contentType: "T",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/your-first-html-page/_index.md",
    projectSubmissionType: null,
    linkName: null,
    linkExample: null,
    linkMessage: null,
    linkSubmission: null,
    reviews: [],
    title: "Your first HTML page",
    status: STATUS_READY,
    blurb:
      "Time to flex your skills! In this step you'll be writing a web page from scratch on your own device.",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/3",
};

export const TopicDone = Template.bind({});
TopicDone.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 3,
  registration,
  stepDetails: {
    contentType: "T",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/your-first-html-page/_index.md",
    projectSubmissionType: null,
    linkName: null,
    linkExample: null,
    linkMessage: null,
    linkSubmission: null,
    reviews: [],
    title: "Your first HTML page",
    status: STATUS_DONE,
    blurb:
      "Time to flex your skills! In this step you'll be writing a web page from scratch on your own device.",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/3",
};

export const ProjectBlocked = Template.bind({});
ProjectBlocked.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 4,
  registration,
  stepDetails: {
    contentType: "P",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/hosting-your-page-on-github-pages/_index.md",
    projectSubmissionType: "L",
    linkName: "Github page url",
    linkExample: "https://your-name.github.io/your-repo-name/",
    linkMessage:
      "Please make sure you are linking to your github page, not just your repo. If someone follows the link then they should sww your website",
    linkSubmission: "https://sheenarbw.github.io/pres-app-engine-node/",
    reviews: [],
    title: "Hosting your website on the web",
    status: STATUS_BLOCKED,
    blurb:
      "This section will be downright empowering. Once you have done this you'll be able to make websites and share them on the internet whenever you want, for free,  forever. Feel the power!",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/4",
};

export const ProjectReady = Template.bind({});
ProjectReady.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 4,
  registration,
  stepDetails: {
    contentType: "P",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/hosting-your-page-on-github-pages/_index.md",
    projectSubmissionType: "L",
    linkName: "Github page url",
    linkExample: "https://your-name.github.io/your-repo-name/",
    linkMessage:
      "Please make sure you are linking to your github page, not just your repo. If someone follows the link then they should sww your website",
    linkSubmission: "https://sheenarbw.github.io/pres-app-engine-node/",
    reviews: [
      {
        timestamp: "2023-03-20T14:53:10.039920Z",
        status: "NYC",
        comments:
          "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code. Something went wrong when I marked your code. Most people don't get things right on the first try, just keep trying, I'm sure you'll figure it out! \n\nHere are some details:\n\n*Pytest errors*\n- Your character set should be UTF-8. Please double check that you followed the instructions, it's all explained\n- Your HTML is not valid. Here's some output from the validator. If it's confusing just go back to basics. Are all your tags closed? Are all the tags included? : - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - The “width” attribute on the “td” element is obsolete. Use CSS instead.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - Bad value “assets/comparison of products.png” for attribute “src” on element “img”: Illegal character in path segment: space is not allowed.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.\n- Please make sure you include at least one paragraph in your site. Something like this: `<p>Your text here</p>`\n- You are missing a required tag. Please make sure each of the following tags are in your website. They need to be in the right places: html, head, meta, title, body\n\nIf the feedback doesn't make sense please reach out to one of the humans that work here and they'll be happy to help you understand. Humans are great like that",
      },
    ],
    title: "Hosting your website on the web",
    status: STATUS_READY,
    blurb:
      "This section will be downright empowering. Once you have done this you'll be able to make websites and share them on the internet whenever you want, for free,  forever. Feel the power!",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/4",
};

export const ProjectUnderReview = Template.bind({});
ProjectUnderReview.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 4,
  registration,
  stepDetails: {
    contentType: "P",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/hosting-your-page-on-github-pages/_index.md",
    projectSubmissionType: "L",
    linkName: "Github page url",
    linkExample: "https://your-name.github.io/your-repo-name/",
    linkMessage:
      "Please make sure you are linking to your github page, not just your repo. If someone follows the link then they should sww your website",
    linkSubmission: "https://sheenarbw.github.io/pres-app-engine-node/",
    reviews: [
      {
        timestamp: "2023-03-20T14:53:10.039920Z",
        status: "NYC",
        comments:
          "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code. Something went wrong when I marked your code. Most people don't get things right on the first try, just keep trying, I'm sure you'll figure it out! \n\nHere are some details:\n\n*Pytest errors*\n- Your character set should be UTF-8. Please double check that you followed the instructions, it's all explained\n- Your HTML is not valid. Here's some output from the validator. If it's confusing just go back to basics. Are all your tags closed? Are all the tags included? : - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - The “width” attribute on the “td” element is obsolete. Use CSS instead.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - Bad value “assets/comparison of products.png” for attribute “src” on element “img”: Illegal character in path segment: space is not allowed.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.\n- Please make sure you include at least one paragraph in your site. Something like this: `<p>Your text here</p>`\n- You are missing a required tag. Please make sure each of the following tags are in your website. They need to be in the right places: html, head, meta, title, body\n\nIf the feedback doesn't make sense please reach out to one of the humans that work here and they'll be happy to help you understand. Humans are great like that",
      },
    ],
    title: "Hosting your website on the web",
    status: STATUS_UNDER_REVIEW,
    blurb:
      "This section will be downright empowering. Once you have done this you'll be able to make websites and share them on the internet whenever you want, for free,  forever. Feel the power!",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/4",
};

export const ProjectError = Template.bind({});
ProjectError.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 4,
  registration,
  stepDetails: {
    contentType: "P",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/hosting-your-page-on-github-pages/_index.md",
    projectSubmissionType: "L",
    linkName: "Github page url",
    linkExample: "https://your-name.github.io/your-repo-name/",
    linkMessage:
      "Please make sure you are linking to your github page, not just your repo. If someone follows the link then they should sww your website",
    linkSubmission: "https://sheenarbw.github.io/pres-app-engine-node/",
    reviews: [
      {
        timestamp: "2023-03-20T14:53:10.039920Z",
        status: "NYC",
        comments:
          "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code. Something went wrong when I marked your code. Most people don't get things right on the first try, just keep trying, I'm sure you'll figure it out! \n\nHere are some details:\n\n*Pytest errors*\n- Your character set should be UTF-8. Please double check that you followed the instructions, it's all explained\n- Your HTML is not valid. Here's some output from the validator. If it's confusing just go back to basics. Are all your tags closed? Are all the tags included? : - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - The “width” attribute on the “td” element is obsolete. Use CSS instead.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - Bad value “assets/comparison of products.png” for attribute “src” on element “img”: Illegal character in path segment: space is not allowed.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.\n- Please make sure you include at least one paragraph in your site. Something like this: `<p>Your text here</p>`\n- You are missing a required tag. Please make sure each of the following tags are in your website. They need to be in the right places: html, head, meta, title, body\n\nIf the feedback doesn't make sense please reach out to one of the humans that work here and they'll be happy to help you understand. Humans are great like that",
      },
    ],
    title: "Hosting your website on the web",
    status: STATUS_ERROR,
    blurb:
      "This section will be downright empowering. Once you have done this you'll be able to make websites and share them on the internet whenever you want, for free,  forever. Feel the power!",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/4",
};

export const ProjectDone = Template.bind({});
ProjectDone.args = {
  contentHtml,
  registrationId: 6,
  stepIndex: 4,
  registration,
  stepDetails: {
    contentType: "P",
    rawUrl:
      "https://raw.githubusercontent.com/Umuzi-org/ACN-syllabus/develop/content/zmc-challenges/first-website/hosting-your-page-on-github-pages/_index.md",
    projectSubmissionType: "L",
    linkName: "Github page url",
    linkExample: "https://your-name.github.io/your-repo-name/",
    linkMessage:
      "Please make sure you are linking to your github page, not just your repo. If someone follows the link then they should sww your website",
    linkSubmission: "https://sheenarbw.github.io/pres-app-engine-node/",
    reviews: [
      {
        timestamp: "2023-03-20T14:53:10.039920Z",
        status: "NYC",
        comments:
          "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code. Something went wrong when I marked your code. Most people don't get things right on the first try, just keep trying, I'm sure you'll figure it out! \n\nHere are some details:\n\n*Pytest errors*\n- Your character set should be UTF-8. Please double check that you followed the instructions, it's all explained\n- Your HTML is not valid. Here's some output from the validator. If it's confusing just go back to basics. Are all your tags closed? Are all the tags included? : - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - The “width” attribute on the “td” element is obsolete. Use CSS instead.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.. - Bad value “assets/comparison of products.png” for attribute “src” on element “img”: Illegal character in path segment: space is not allowed.. - An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.\n- Please make sure you include at least one paragraph in your site. Something like this: `<p>Your text here</p>`\n- You are missing a required tag. Please make sure each of the following tags are in your website. They need to be in the right places: html, head, meta, title, body\n\nIf the feedback doesn't make sense please reach out to one of the humans that work here and they'll be happy to help you understand. Humans are great like that",
      },
    ],
    title: "Hosting your website on the web",
    status: STATUS_DONE,
    blurb:
      "This section will be downright empowering. Once you have done this you'll be able to make websites and share them on the internet whenever you want, for free,  forever. Feel the power!",
  },
  submitProjectLink: {
    isLoading: false,
  },
  currentPath: "/user-challenge/6/steps/4",
};
