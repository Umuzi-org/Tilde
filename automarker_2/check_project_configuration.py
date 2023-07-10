from fire import Fire
from automarker.marker import check_project_configuration


def run(content_item_id, flavours):
    check_project_configuration(
        content_item_id=content_item_id, flavours=flavours.split(",")
    )


if __name__ == "__main__":
    Fire(run)
