"""
TODO: Change the data source. We need to work from accurate data
"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session, SessionType


def create_card_progress_based_sessions():
    """
    Get card progress data from airtable 
    
    Look at duration data. If people are finished with us then skip them 
    Find peeople who are falling behind in each stream 

    Order people by urgency:
    - The further behind a person is, the more urgent it is
    - The further a person is in their time with us, the less time we have with them
    
    Group people according to where they are in their progress. 
    """

    


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_card__progress_based_sessions()
        print("Done")
