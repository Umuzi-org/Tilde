import React from "react";
import Markdown from "react-markdown";
import * as matter from "gray-matter";

const fixUrls = (src, content) => {
  // const baseUrl = src.slice(0, src.lastIndexOf("/"));
  return content;
  // TODO: replace relative urls with absolute so that the images render properly #184
};

export function MarkdownRenderer({ src }) {
  const [markdown, setMarkdown] = React.useState(null);

  React.useEffect(() => {
    if (markdown === null) {
      fetch(src)
        .then((res) => res.text())
        .then((text) => {
          const parsed = matter(text);
          const content =
            `# ${parsed.data.title}` + fixUrls(src, parsed.content);
          setMarkdown(content);
        });
    }
  });

  // (#185)
  return <Markdown source={markdown || "Loading..."}></Markdown>;
}
