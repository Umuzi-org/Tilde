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
        raise SystemError(
            f"Config not found for this project: content_item_id={content_item_id} flavours={flavours}"
        )

    assert (
        config.status in constants.CONFIG_ALLOWED_STATUSES
    ), f"Invalid status: {config.status}"

    if config.status == constants.CONFIG_STATUS_NOT_IMPLEMENTED:
        raise NotImplementedError("This project has not been implemented yet")

    clone_dir_name = (
        f"{content_item_id}-{'-'.join(sorted(flavours))}-perfect"
        if self_test
        else url.replace("git@github.com:", "").replace("/", "-")
    )

    perfect_project_path = Path(config.__file__).parent / "perfect_project"

    clone_dir_path = DOWNLOAD_DIR / clone_dir_name
    project_uri = perfect_project_path if self_test else url

    for step in config.steps:
        print(f"--- Running step: {step} ---")

        step.execute_run(
            project_uri=project_uri,
            clone_dir_path=clone_dir_path,
            self_test=self_test,
            config=config,
            fail_fast=fail_fast,
        )
        if step.status != constants.STEP_STATUS_PASS:
            break

    return config.steps


def mark_learner_project(content_item_id, flavours, url):
    final_mark = mark_project(content_item_id, flavours, url)
    format_as_review(final_mark)


def run_configuration_test(content_item_id, flavours):
    steps = mark_project(
        content_item_id=content_item_id,
        flavours=flavours,
        self_test=True,
        fail_fast=True,
    )

    final_status = constants.STEP_STATUS_PASS

    print()
    for step in steps:
        if constants.STEP_FINAL_STATUSES.index(
            step.status
        ) > constants.STEP_FINAL_STATUSES.index(final_status):
            final_status = step.status

        print(f"STEP: {step.name} ")
        print(f"\tDuration: {step.duration()}")
        print(f"\tStatus: {step.status}")
        if step.message:
            print(f"\tMessage: {step.message}")
        if step.details:
            print(f"\tDetails:")
            print(step.details_string())
        print()

    print(f"FINAL STATUS: {final_status}")


run_configuration_test(
    content_item_id=705,
    flavours=["python"],
)


# run_configuration_test(
#     content_item_id=705,
#     flavours=["javascript"],
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


# mark_project(
#     content_item_id=223,
#     flavours=["javascript"],
#     self_test=True,
#     fail_fast=True,
# )

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


# if __name__ == "__main__":
#     from fire import Fire

#     Fire(mark_learner_project)


# mark_project(
#     content_item_id=186,
#     flavours=["javascript"],
#     self_test=True,
#     fail_fast=True,
# )
