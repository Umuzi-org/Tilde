import os
import re
from pathlib import Path
from importlib import import_module
import sys
import constants

CONFIG_DIR = Path("../../../automarker_2_config")  # TODO: Make this configurable
DOWNLOAD_DIR = Path("../gitignore").resolve()

sys.path.append(str(CONFIG_DIR.resolve()))


def flavours_match(config_flavours, flavours):
    flavours = sorted(flavours)
    for flavour_set in config_flavours:
        flavour_set = sorted(flavour_set)
        if flavours == flavour_set:
            return True
    return False


def get_project_config_dir_path(content_item_id):
    names = os.listdir(CONFIG_DIR)
    for project_dir_name in names:
        full_path = CONFIG_DIR / project_dir_name
        if not full_path.is_dir():
            continue
        found = re.search(r"^(.+)_(\d+)$", project_dir_name)
        if not found:
            continue
        title, config_content_item_id = found.groups()
        config_content_item_id = int(config_content_item_id)
        if config_content_item_id == content_item_id:
            return project_dir_name


def get_project_flavour_config(project_directory, flavours):
    full_path = CONFIG_DIR / project_directory
    for sub_directory_name in os.listdir(full_path):
        sub_directory = full_path / sub_directory_name
        if not sub_directory.is_dir():
            continue
        flavour_config_file = sub_directory / "config.py"
        if not flavour_config_file.is_file():
            continue
        configuration = import_module(
            f"{project_directory}.{sub_directory_name}.config"
        )
        config_flavours = configuration.flavours
        if flavours_match(config_flavours, flavours):
            return configuration


def get_project_configuration(content_item_id, flavours):
    project_directory = get_project_config_dir_path(content_item_id)
    if not project_directory:
        return
    return get_project_flavour_config(project_directory, flavours)


def mark_project(content_item_id, flavours, url=None, self_test=False, fail_fast=False):
    """This is the entrypoint, this function actually does the work of marking the code"""

    # find the matching configuration
    # config is a python module
    config = get_project_configuration(content_item_id, flavours)

    if not config:
        raise Exception("Config not found")  # TODO: Better exception types

    assert (
        config.status in constants.ALLOWED_STATUSES
    ), f"Invalid status: {config.status}"

    if config.status == constants.STATUS_NOT_IMPLEMENTED:
        raise NotImplementedError("This project has not been implemented yet")

    clone_dir_name = (
        f"{content_item_id}-{'-'.join(sorted(flavours))}-perfect"
        if self_test
        else url.replace("git@github.com:", "").replace("/", "-")
    )

    perfect_project_path = Path(config.__file__).parent / "perfect_project"

    for step in config.steps:
        step.run(
            project_uri=perfect_project_path if self_test else url,
            clone_dir_path=DOWNLOAD_DIR / clone_dir_name,
            self_test=self_test,
            config=config,
            fail_fast=fail_fast,
        )


# mark_project(
#     content_item_id=705,
#     flavours=["python"],
#     self_test=True,
#     fail_fast=True,
# )

# mark_project(
#     content_item_id=705,
#     flavours=["javascript"],
#     self_test=True,
#     fail_fast=True,
# )

# mark_project(
#     content_item_id=756,
#     flavours=["javascript"],
#     self_test=True,
#     fail_fast=True,
# )

# mark_project(
#     content_item_id=756,
#     flavours=["python"],
#     self_test=True,
#     fail_fast=True,
# )

# mark_project(
#     content_item_id=756,
#     flavours=["java"],
#     self_test=True,
#     fail_fast=True,
# )


mark_project(
    content_item_id=223,
    flavours=["javascript"],
    self_test=True,
    fail_fast=True,
)

# mark_project(
#     content_item_id=223,
#     flavours=["python"],
#     self_test=True,
#     fail_fast=True,
# )

# mark_project(
#     content_item_id=223,
#     flavours=["java"],
#     self_test=True,
#     fail_fast=True,
# )
