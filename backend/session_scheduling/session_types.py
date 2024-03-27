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
# SESSION_PROBLEM_SOLVING = "Problem solving" TODO
# SESSION_CARD_BASED = "card progress based" TODO


session_types = [
    SessionTypeConf(
        name=SESSION_FUNDAMENTAL_SKILL_SPOT_CHECK,
        event_copy="It looks like you know what you are doing. We just want to spend a little time with you to make sure. If it turns out that you don't know something then we're here to help.",
        event_title="Skill Spot Check",
        description="The student seems to know what they are doing. We are just checking on them to make sure our other systems are working.",
        duration_minutes=45,
    ),
    SessionTypeConf(
        name=SESSION_FUNDAMENTAL_SKILL_ASSISTANCE,
        event_copy="It looks like you might need some help with understanding {extra_title_text}. In this session we'll help you get a firm handle on the content",
        event_title="Skill Assistance - {extra_title_text} {flavours}",
        description="The student needs help with a specific skill. We are here to help them.",
        duration_minutes=60,
    ),
    SessionTypeConf(
        name=SESSION_BOOTCAMP_ASSESSMENT,
        event_copy="Well done for getting this far in the bootcamp. The next step is a chat with one of our staff members. Please make sure you are in a quiet place with good internet, and make sure you are on time. To prepare for this session, make sure you UNDERSTAND all the things you did during the bootcamp. Read over all the things and make sure you can answer all the questions.",
        event_title="Bootcamp Assessment - {extra_title_text}",
        description="This is the final assessment for a learner who is taking part in a selection bootcamp. We are assessing them to see if they are ready to join the main bootcamp.",
        duration_minutes=45,
    ),
]
