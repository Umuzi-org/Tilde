import concurrent.futures

from django.core.management.base import BaseCommand, CommandParser

from automarker_app.lib.marker import (
    get_all_marker_configs,
    mark_project,
    get_steps_final_status,
)
from automarker_app.lib.constants import (
    CONFIG_STATUS_DEBUG,
    CONFIG_STATUS_PRODUCTION,
    STEP_STATUS_PASS,
    STEP_STATUS_WAITING,
)


from ..utils import print_steps_result


DASH_SEPARATOR = "-" * 100


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--skip", type=int, nargs="+")

    def handle(self, *args, **options):
        good_configs = []
        bad_configs = []

        skip_ids = options.get("skip", [])

        for config in get_all_marker_configs():
            if (
                config.status
                in [
                    CONFIG_STATUS_DEBUG,
                    CONFIG_STATUS_PRODUCTION,
                ]
                and config.content_item_id not in skip_ids
                and config.flavours[0][0] == "python"
            ):
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    _future = executor.submit(
                        mark_project,
                        config.content_item_id,
                        config.flavours[0],
                        self_test=True,
                        fail_fast=True,
                    )

                    steps = _future.result()

                    if any([step.status != STEP_STATUS_PASS for step in steps]):
                        bad_configs.append(
                            (
                                [
                                    config.title,
                                    config.flavours,
                                    config.content_item_id,
                                ],
                                [
                                    step
                                    for step in steps
                                    if step.status
                                    not in [STEP_STATUS_PASS, STEP_STATUS_WAITING]
                                ],
                            )
                        )
                    else:
                        good_configs.append(
                            [
                                config.title,
                                config.flavours,
                                config.content_item_id,
                            ]
                        )

        for config in good_configs:
            print(DASH_SEPARATOR)
            print("PASS:", config)
        print(DASH_SEPARATOR)

        for config, failed_steps in bad_configs:
            print(DASH_SEPARATOR)
            print(
                "FAIL:",
                config[:-1],
            )
            print(DASH_SEPARATOR)
            print(print_steps_result(failed_steps))

            print()
            print(DASH_SEPARATOR)
            print(DASH_SEPARATOR)
