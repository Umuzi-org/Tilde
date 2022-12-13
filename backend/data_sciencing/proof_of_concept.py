# %%

# CRITICAL: Dont attempt to import any models until you have called setup_database_connections. It just wont work

from utils import setup_database_connections

setup_database_connections()

# %%

import pandas as pd
from django.contrib.auth import get_user_model
from curriculum_tracking.models import RecruitProjectReview

User = get_user_model()

# %%


reviews = RecruitProjectReview.objects.filter(reviewer_user__is_staff=True).filter(
    reviewer_user__active=True
)

reviews_df = pd.DataFrame(list(reviews.values()))

reviews_df.head()
# %%


# %%
