# Project review coordination

This app allows staff members and freelancers to coordinate their own code review efforts. 

The user journey is as follows:

1. A staff member (or freelancer) logs into Tilde and navigates to the project review coordination page
2. Here they will see a bunch of "bundles". A bundle is a group of projects in the "Review" column on a Tilde user's board. The projects that have been sitting in the review column for the longest are at the top of the page
3. The staff member can "claim" a bundle of projects. This means that they intend to review all those projects immediately. Once projects have been claimed by a staff member, they cannot be claimed by someone else until the staff member has reviewed those projects.
4. The staff member can then navigate to "My claims" to see all the things that they are meant to review. As they review the projects the claim will be updated
- if the staff member reviewed the project, and it stayed in the "review" column, then that project can be claimed in another bundle by another staff member
- if the project moved to "complete" or "review feedback" then it will not need another review 

This system allows staff members to choose what to review and will avoid situations where multiple staff members are adding the same review to the same project.