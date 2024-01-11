# Naming conventions and structure

The templates here can become quite spaghetti-like if we are not careful. 

Below are some definitions and conventions we follow:

## General naming conventions

Different templates have different types. The name of a single template file should follow the following pattern:

- {type}.html, eg "page.html". In this case the directory that the template is in will tell you what it is for. Eg user/board/page.html
- {type}_{name}.html, eg "page_login.html"

## Template types

### Page

Naming convention: `page.html` or `page_???.html`


This is a full-on web page, it is something a user will navigate to in their browser.

These templates are either named page.html or something like page_login.html

### Partial

Naming convention: `partial_???.html`

This is a part of a page, for example a header or footer area. A partial is a major part of the page layout. 

### View partial

Naming convention: `view_partial_???.html`

These are partials that are associated with Django Views. These are typically fetched from the frontend using HTMX. 

### JS exec 

Naming convention: `js_exec_???.html`


These are templates that include a `<script>` tag that executes code. This is not a place to define functions or write long pieces of code, its really just for calling functions that are defined elsewhere.

### Email 

Naming convention: `email_???.html`

From time to time we need to send emails. 

### Base 

Naming convention: `base.html` or `base_???.html`


Base templates contain common functionality that would be used by many pages. 

