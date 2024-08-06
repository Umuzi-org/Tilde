from core.models import Team

"""
Navigation configuration for the frontend.

This dictionary defines the structure and properties of the navigation menu.
Top-level keys represent main pages/headers.
Second-level keys represent secondary pages/headers.

Each second-level dictionary contains:
- 'url_name': The URL name according to Django's naming convention
- 'label': The text to be displayed for the link
- 'permissions': Required permissions to access the page

Example:
navigation = {
    'main_page': {
        'secondary_page': {
            'url_name': 'django_url_name',
            'label': 'Link Display Text',
            'permissions': ['required_permission1', 'required_permission2']
        },
        # ... other secondary pages ...
    },
    # ... other main pages ...
}
"""

navigation = {
    "users_and_teams_nav": {
        "users_and_teams_nav":{
            "url_name": "users_and_teams_nav",
            "label": "Teams",
            "permissions": Team.PERMISSION_VIEW,
        },
    },
    "user_board": {
        "user_board":{
            "url_name": "user_board",
            "label": "Board",
            "permissions": Team.PERMISSION_VIEW,
        },
        "review_performance":{
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
            "permissions": Team.PERMISSION_VIEW,
        },
        "project_review_coordination_my_claims": {
            "url_name": "project_review_coordination_my_claims",
            "label": "My claims",
            "permissions": Team.PERMISSION_VIEW,
        },
        "project_review_coordination_all_claims": {
            "url_name": "project_review_coordination_all_claims",
            "label": "All claims",
            "permissions": Team.PERMISSION_VIEW,
        },
    },
    "dashboard_project_review_health": {},
}

"""
MAIN TASKS
- create data structure - done
- pass the main nav dictionary to each page that requires main headers - done
- reorg how navigation is accessed for secondary headers - done
- document data strucure in a comment - done
- simplify code using data structure - somewhat done
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
