# NOW:

- finish user testing. Then test it again.
- npm tests pass

- deploy:
  - migrate db structure
  - populate Team model based on old UserGroup stuff
  - get rid of UserGroup model
  - look at permissions of JTLs, Scrummies, and staff. make sure they make sense
    CELEBRATE!!

# ROADMAP

How this doc works:

Basically this is a high-level backlog of what we need to do. When we do backlog refinement and prepare for sprints then stuff will get moved over to an actual issue list. This is just for convenience.

## make it easier to work with

- frontend: include topics needing reviews on crd summary page [permissionStudent](http://localhost:3000/teams/1/card_summary)
- frontend: include open PRs icon on cards

## Tech dept

- upgrade all api views to use permission filtering

## Make it easier to contribute

- read https://github.com/hyperledger/indy-node/blob/master/docs/source/write-code-guideline.md
- https://github.com/hyperledger/indy-node/blob/master/docs/source/ci-cd.md
- https://github.com/hyperledger/indy-node/blob/master/README.md#how-to-start-working-with-the-code

## bugs

- login page needs to be responsive
- github auth is weird, couldn't log in as Umuzibot. Doesn't matter too much right now but can cause problems later
- review button doesn't come up in all the places it should for topics. We need it to work the same as the project stuff
