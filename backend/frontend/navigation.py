navigation = {
    "users_and_teams_nav": {
        "users_and_teams_nav":{
            "url_name": "users_and_teams_nav",
            "label": "Teams",
            "permissions": [],
        },
    },
    "user_board": {
        "user_board":{
            "url_name": "user_board",
            "label": "Board",
            "permissions": [],
        },
        "review_perfomance":{
            "url_name": "user_board",
            "label": "Review perfomance",
            "permissions": [],
        },
    },
    "user_review_trust_list": {},
    "team_dashboard": {
        "team_dashboard":{
            "url_name": "team_dashboard",
            "label": "Dashboard",
            "permissions": [],
        },
        "card_summary":{
            "url_name": "team_dashboard",
            "label": "Card summary",
            "permissions": [],
        },
    },
    "view_partial_team_user_progress_chart": {},
    "project_review_coordination": {
        "project_review_coordination_unclaimed": {
            "url_name": "project_review_coordination_unclaimed",
            "label": "Unclaimed bundles",
            "permissions": [],
        },
        "project_review_coordination_my_claims": {
            "url_name": "project_review_coordination_my_claims",
            "label": "My claims",
            "permissions": [],
        },
        "project_review_coordination_all_claims": {
            "url_name": "project_review_coordination_all_claims",
            "label": "All claims",
            "permissions": [],
        },
    },
    "dashboard_project_review_health": {},
}

"""
MAIN TASKS
- create data structure - done
- pass the main nav dictionary to each page that requires main headers - not done
- reorg how navigation is accessed for secondary headers - not done
- document data strucure in a comment - not done
- simplify code using data structure - not done
- active links should get highlighted - not done
  - main nav links highlights - done
  - secondary nav links highlights - done
  - active parent links should also be highlighted when instance link is active - not done
  - will need to pass in a list of links for each nav header to keep things dry - done


Potential new tasks:
- Have instance overview pages. E.g user profile with all info about user at /user/<id>. Same with team.
- /users/<id> - we could have: links to board, review performance, activity, start date and end, teams and other info
- /teams/<id> - link to team info, learners in the team
"""
