import concurrent.futures
import subprocess
from django.core.management.base import BaseCommand, CommandParser
from automarker_app.lib.marker import (
    get_all_marker_configs,
    mark_project,
)
from automarker_app.lib.constants import (
    CONFIG_STATUS_DEBUG,
    CONFIG_STATUS_PRODUCTION,
    STEP_STATUS_PASS,
    STEP_STATUS_WAITING,
)
from ..utils import print_steps_result


CUSTOM_SEPARATOR = lambda char: char * 100
DASH_SEPARATOR = CUSTOM_SEPARATOR("-")


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--skip", type=int, nargs="+", required=False)

    def handle(self, *args, **options):
        good_configs = []
        bad_configs = []
        skip_ids = []

        if options["skip"] is not None:
            skip_ids = options["skip"]

        for config in get_all_marker_configs():
            if (
                config.status
                in [
                    CONFIG_STATUS_DEBUG,
                    CONFIG_STATUS_PRODUCTION,
                ]
                and config.content_item_id not in skip_ids
            ):
                formatted_config = (
                    f"{config.title}[{config.content_item_id}] {config.flavours}"
                )

                print("\nCHECKING:", formatted_config)

                _future = None
                steps = []
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    _future = executor.submit(
                        mark_project,
                        config.content_item_id,
                        config.flavours[0],
                        self_test=True,
                        fail_fast=True,
                    )

                try:
                    steps = _future.result(timeout=120)
                except subprocess.TimeoutExpired:
                    bad_configs.append(f"{formatted_config} took too long (>120s)")

                if any([step.status != STEP_STATUS_PASS for step in steps]):
                    bad_configs.append(
                        (
                            formatted_config,
                            [
                                step
                                for step in steps
                                if step.status
                                not in [STEP_STATUS_PASS, STEP_STATUS_WAITING]
                            ],
                        ),
                    )
                else:
                    good_configs.append(formatted_config)
        if len(bad_configs):
            print()
            print(CUSTOM_SEPARATOR("*"))
            print(
                f"{'-' * 3} Some configurations appear to be incorrect. Please review the output below for details:".upper()
            )
            print(CUSTOM_SEPARATOR("*"))

            for config, failed_steps in bad_configs:
                print(DASH_SEPARATOR, "\n")
                print("BAD:", config)
                if failed_steps:
                    print_steps_result(failed_steps)
        else:
            print(CUSTOM_SEPARATOR("*"))
            print("All configurations passed!".upper())
            print(CUSTOM_SEPARATOR("*"), "\n")
