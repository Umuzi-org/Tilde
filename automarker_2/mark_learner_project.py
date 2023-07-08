from fire import Fire
from automarker.marker import mark_learner_project


def run(content_item_id, flavours, url):
    mark_learner_project(
        content_item_id=content_item_id, flavours=flavours.split(","), url=url
    )


if __name__ == "__main__":
    Fire(run)
