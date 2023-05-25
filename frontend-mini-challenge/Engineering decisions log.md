# Why Next?

Next is React based - compatible with team's existing skillset + hella powerful
There are a few different frameworks built on top of React:

- Create React app: This is a painful thing to upgrade and somewhat bloated
- Remix - this is a new kid on the block and is quickly gaining popularity. But it's not as popular as Next (so in theory it's easier to hire Next devs and get NExt support?) It also only handles server-side rendering whereas Next handles SSR as well as static pages.

At some point what you need is something "good enough" and fairly future proof.

Here is a nice comparison: https://ikius.com/blog/next-js-alternatives

# Data fetching

The main Tilde frontend makes use of some redux-saga based data fetching and caching tools. These would work but:

- those tools were created before redux-toolkit was developed. There are better tools now that are not homegrown
- again, we need something "good enough"
- we can possibly have one tool for fetching and then make use of redux for state management if we need to
- the downside of the approach taken on Tilde is that it's hard for people to learn how it works. It seems to magical.

Options considered:

- SWR: It's the Next.js way of doing things
- Redux toolkit RTK: Redux is hella powerful and given our use of the tool, it makes sense to see if we can just modernize what we are already doing

According to this https://sveltequery.vercel.app/comparison RTK has more features. But none of those seem like a deal-breaker. Most of what looks useful there can likely be handled by another tool or workaround.

https://npmtrends.com/redux-toolkit-vs-swr

- swr is far more commonly used.

Learning curve and dev experience:
SWR is much easier to learn.
RTK has a more complicated set up and needs more boilerplate.

Often, when using a framework it's best to just go with what the framework suggests.

And the winner is.... SWR

# UI testing

The bare minimum is to make sure nothing is explicitly broken. Use https://storybook.js.org/docs/react/writing-tests/test-runner

To run it:

```
# terminal 1

npm run storybook

# terminal 2

npm run test-storybook
```
