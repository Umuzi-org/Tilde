# Tilde

## What is Tilde?

It is an open-source, agile, collaborative learning platform. Chock full of wholesome goodness. 

Tilde was built as a response to COVID (we needed to be)

It was designed by devs for devs. The idea is that people should learn to code in a way that feels the same as working on a real dev team. From the student's point of view, it is a kanban board with interesting integrations. But there is a lot more to it than that.

This is for our learners/students (we sometimes call them recruits):

- https://umuzi-org.github.io/tech-department/syllabuses/tilde-intro-student/
- https://www.youtube.com/playlist?list=PLqU7nTtS-XlkQg6qDxvskKzITPU3YmMQB

The syllabus in the top link gets converted into a bunch of cards that show up on the student's board

And this is for our staff (we call them staff):

- [https://www.youtube.com/playlist?list=PLqU7nTtS-XlnztOgNcuV_LSpRyc0qeS8_](https://www.youtube.com/playlist?list=PLqU7nTtS-XlnztOgNcuV_LSpRyc0qeS8_)

## Quick links

- [Quick start](/quick-start.md)
- [Contributing](/CONTRIBUTING.md)


## Tech stack

![Tech stack](/tech-stack.png?raw=true "Tech stack")

We use JS, not Typescript.

## Syllabus as code

Instead of building a heavy forms-based application to allow editing of syllabus content, we opted to use markdown files and yaml frontmatter. We were using [Hugo](https://gohugo.io/) pre-covid and so we just adapted that to suit our purposes.

Here is our main syllabus repository:

https://github.com/Umuzi-org/ACN-syllabus

You can run this as a standalone static site, or use it as an input to Tilde.

To get Tilde to ingest the Hugo syllabus site you need to clone the syllabus repo and then make use of the following Django management command:

```
cd backend 
# activate your virtual environment however you like to
python manage.py load_content_from_syllabus_repo_hugo /path/to/ACN-syllabus 1 1
```

If the comment about your virtual environment doesn't make sense, please refer to the [backend README](/backend/README.md). Or Google it :) virtual environments are old news in Python and there are plenty of great resources on the web.

## Awards

Tilde is a core component of the [African Coding Network](https://www.africancoding.network/). ACN won the "Most Scalable Solution" prize in the Ashoka Future Skills Innovation Challenge.

