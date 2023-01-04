## Pull Requests: What do to and how to review them

Pull requests are a vital and important part of any software engineering team. They allow us to control what code goes into the main branch and when. Obviously, this process is extremely important and it is also important that we get the process right. This document will hopefully serve to nail down the process for creating a PR, Reviewing a PR as well as addressing feedback on a PR

### Opening a new Pull Request

When opening a Pull request, there is a checklist of points that appears on the PR template. While all of these points may not be relevant to your particular PR, The following points have to be followed for every single PR:

- [ ] My code follows the style guidelines of this project
- [ ] I have merged the develop branch into my branch and fixed any merge conflicts
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] I have tested new or existing tests and made sure that they pass

By ticking the points on the checklist, you are acknowledging that you have followed the description on that point. So don’t just tick the boxes.

Once your PR has been opened, link it to the relevant issue and move the issue into the Review column for other Technical Staff to have a look at

### Addressing feedback on your Pull Request

When addressing an existing PR that has some feedback on it, it is vitally important to address said feedback before moving the card back into review. The important thing to remember is that its not enough to just address it in code.

For this, we will be using the github conversation as a way to provide feedback as well as show that a person has addressed the feedback. On an existing Pull Request, you will be receiving feedback on the “Conversation” tab as well as the “Files Changed” tab. If you are done addressing the feedback, you need to make the reviewer aware that you have done so. If you click the “Resolve Conversation” button, you acknowledge that you have addressed the feedback provided on that part of the conversation. PRs that don’t have all conversations resolved will be pushed back into the review feedback column

If you have addressed the feedback in the form of a chat outside of github, please mention it regardless. Eg “Khalid has made a change and Sheena has provided feedback on why this piece of code is here. They had a conversation offline and agree that Khalid has done the right thing". Khalid needs to make sure that the rest of the team knows that this conversation happened.

### Reviewing a Pull Request

When reviewing a Pull request there are a couple of things to keep in mind:

• You need to understand the requirements of the issue first and make sure that the code solves said issue. Run the code on your local machine and test using various test cases to make sure it works.
• The second thing to make sure of is that all previous feedback needs to be addressed in this PR. There may be a long conversation that took place on the same PR and you need to be aware of this change
