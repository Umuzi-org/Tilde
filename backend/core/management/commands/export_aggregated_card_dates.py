from django.core.management.base import BaseCommand
from core.models import Team
from curriculum_tracking.models import AgileCard
from django.utils import timezone
import pandas as pd


def calculate_card_duration(row):
    start_time = row["card.start_time"]
    complete_time = row["card.complete_time"]
    if pd.isnull(start_time) or pd.isnull(complete_time):
        return 0
    delta = complete_time - start_time
    return delta.seconds


def clean_flavour_names(key):
    def _clean_flavour_names(row):
        names = row[key]
        names.sort()
        return ", ".join(names)

    return _clean_flavour_names


class Command(BaseCommand):
    def handle(self, *args, **options):

        data = []
        for team in Team.objects.filter(active=True):
            # for team in Team.objects.filter(name="Cohort 22 web dev"):
            print(f"processing team: {team.name}")
            for card in AgileCard.objects.filter(assignees__in=team.user_set.all()):

                data.append(
                    {
                        "team.name": team.name,
                        "card.complete_time": card.complete_time,
                        "card.review_request_time": card.review_request_time,
                        "card.start_time": card.start_time,
                        "card.flavour_names": card.flavour_names,
                        "card.content_item.title": card.content_item.title,
                        "card.content_item.id": card.content_item.id,
                    }
                )

        df = pd.DataFrame(data)

        df["card.complete_time"] = pd.to_datetime(
            df["card.complete_time"], infer_datetime_format=True
        )
        df["card.start_time"] = pd.to_datetime(
            df["card.start_time"], infer_datetime_format=True
        )
        df["duration"] = df.apply(calculate_card_duration, axis=1)
        df = df[df["duration"] != 0]
        df["card.flavour_names"] = df.apply(
            clean_flavour_names("card.flavour_names"), axis=1
        )

        grouped = df.groupby(
            [
                "card.flavour_names",
                "card.content_item.id",
                "card.content_item.title",
                "team.name",
            ],
            as_index=False,
        )

        data = {
            "card.flavour_name": pd.DataFrame(grouped)
            .reset_index()
            .apply(lambda row: row[0][0], axis=1),
            "card.content_item.id": pd.DataFrame(grouped)
            .reset_index()
            .apply(lambda row: row[0][1], axis=1),
            "card.content_item.title": pd.DataFrame(grouped)
            .reset_index()
            .apply(lambda row: row[0][2], axis=1),
            "team.name": pd.DataFrame(grouped)
            .reset_index()
            .apply(lambda row: row[0][3], axis=1),
            "mean": grouped["duration"].mean()["duration"],
            "max": grouped["duration"].max()["duration"],
            "min": grouped["duration"].min()["duration"],
            "median": grouped["duration"].median()["duration"],
            "std": grouped["duration"].std()["duration"],
            "count": grouped["duration"].count()["duration"],
        }
        breakpoint()

        df = pd.concat(data, axis=1)

        today = timezone.now().date()
        df.to_csv(
            f"gitignore/aggreggated_card_export_{today.strftime('%a %d %b %Y')}.csv",
            index=False,
        )

        # headings = data[0].keys()

        # with open(
        #     Path(f"gitignore/.csv"),
        #     "w",
        # ) as f:
        #     writer = csv.writer(f)
        #     writer.writerow(headings)
        #     writer.writerows([[d[heading] for heading in headings] for d in data])
