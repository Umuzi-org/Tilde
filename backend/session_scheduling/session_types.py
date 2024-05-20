"""
This is used for the initialisation of session types in the database. 

The session type names are readonly, everything else can be updated in the db.
"""

from collections import namedtuple

SessionTypeConf = namedtuple(
    "SessionTypeConf",
    [
        "name",
        "event_copy",
        "event_title",
        "description",
        "duration_minutes",
    ],
)

SESSION_FUNDAMENTAL_SKILL_SPOT_CHECK = "Fundamental skill spot check"
SESSION_FUNDAMENTAL_SKILL_ASSISTANCE = "Fundamental skill assistance"
SESSION_BOOTCAMP_ASSESSMENT = "Bootcamp"
SESSION_PROJECT_PROGRESS = "Project progress session"
SESSION_PROBLEM_SOLVING_FOUNDATION_SESSION = "Problem solving foundation"
# SESSION_TROUBLESHOOT_BOUNCY_PR = "PR review troubleshooting"
SESSION_TROUBLESHOOT_BOUNCY_CARD = "Project review troubleshooting"

SESSION_CUSTOM = "Custom"
# SESSION_CARD_BASED = "card progress based" TODO


session_types = [
    SessionTypeConf(
        name=SESSION_FUNDAMENTAL_SKILL_SPOT_CHECK,
        event_copy="It looks like you know what you are doing. We just want to spend a little time with you to make sure. If it turns out that you don't know something then we're here to help.",
        event_title="Skill Spot Check - Skill Spot Check - {extra_title_text} {flavours}",
        description="The student seems to know what they are doing. We are just checking on them to make sure our other systems are working.",
        duration_minutes=45,
    ),
    SessionTypeConf(
        name=SESSION_FUNDAMENTAL_SKILL_ASSISTANCE,
        event_copy="It looks like you might need some help with understanding {extra_title_text}. In this session we'll help you get a firm handle on the content",
        event_title="Skill Assistance - PSF level {extra_title_text} {flavours}",
        description="The student needs help with a specific skill. We are here to help them.",
        duration_minutes=60,
    ),
    SessionTypeConf(
        name=SESSION_PROBLEM_SOLVING_FOUNDATION_SESSION,
        event_copy="You didn't do well on a recent Problem Solving Foundation Level {extra_title_text} test. Let's see if we can help",
        event_title="Problem solving foundation {extra_title_text} - {flavours}",
        description="The learner failed a PSF test. These sessions are scheduled for level 0 and level 1 tests",
        duration_minutes=60,
    ),
    SessionTypeConf(
        name=SESSION_BOOTCAMP_ASSESSMENT,
        event_copy="Well done for getting this far in the bootcamp. The next step is a chat with one of our staff members. Please make sure you are in a quiet place with good internet, and make sure you are on time. To prepare for this session, make sure you UNDERSTAND all the things you did during the bootcamp. Read over all the things and make sure you can answer all the questions.",
        event_title="Bootcamp Assessment - {extra_title_text}",
        description="This is the final assessment for a learner who is taking part in a selection bootcamp. We are assessing them to see if they are ready to join the main bootcamp.",
        duration_minutes=45,
    ),
    SessionTypeConf(
        name=SESSION_PROJECT_PROGRESS,  # https://airtable.com/appkr1uRo6nZXyeZb/tblStRQEBcQmJBDVn/viwgATZ10rBZdAZBq?blocks=hide
        event_copy="You are a behind in your syllabus work. Let's see how we can help",
        event_title="Syllabus progress help {extra_title_text}",
        description="This is for learners who are falling behind in their syllabus work",
        duration_minutes=45,
    ),
    # SessionTypeConf(
    #     name=SESSION_TROUBLESHOOT_BOUNCY_PR,
    #     event_copy="Something is going wrong with this card, it seems to be bouncing around a lot. Let's see if we can get to the bottom of this.",
    #     event_title="Troubleshooting PR review for card {extra_title_text} - {flavours}",
    #     duration_minutes=45,
    # ),
    SessionTypeConf(
        name=SESSION_TROUBLESHOOT_BOUNCY_CARD,
        event_copy="Something is going wrong with the reviews, it seems to be bouncing around a lot. Let's see if we can get to the bottom of this.",
        event_title="Troubleshooting reviews {extra_title_text} - {flavours}",
        duration_minutes=45,
        description="A card has been receiving a lot of PR reviews or a lot of negative competence reviews. The people involved might need some coaching",
    ),
    SessionTypeConf(
        name=SESSION_CUSTOM,
        event_copy="",
        event_title="{extra_title_text}",
        description="This is for ad-hoc sessions set up by a human. The event title will come from the field `extra_title_text` and the event copy (the body of the invitation) will come from the `extra_event_body_text` field",
        duration_minutes=45,
    ),
]
