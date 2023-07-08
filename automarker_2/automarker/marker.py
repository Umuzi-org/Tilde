import os
import re
from pathlib import Path
from importlib import import_module
import sys
from . import constants

CONFIG_DIR = Path(
    os.environ["AUTOMARKER_2_CONFIG_DIR"]
).resolve()  # TODO: Make this configurable
DOWNLOAD_DIR = Path("./gitignore").resolve()

sys.path.append(str(CONFIG_DIR))


def _flavours_match(config_flavours, flavours):
    flavours = sorted(flavours)
    for flavour_set in config_flavours:
        flavour_set = sorted(flavour_set)
        if flavours == flavour_set:
            return True
    return False


def _scan_config_dir_for_project_directories():
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
        yield project_dir_name, config_content_item_id, title


# def get_project_config_dir_path(content_item_id):
#     for (
#         project_dir_name,
#         config_content_item_id,
#         title,
#     ) in _scan_config_dir_for_project_directories():
#         if config_content_item_id == content_item_id:
#             return project_dir_name


def get_all_marker_configs():
    for (
        project_dir_name,
        config_content_item_id,
        title,
    ) in _scan_config_dir_for_project_directories():
        full_project_path = CONFIG_DIR / project_dir_name
        for sub_directory_name in os.listdir(full_project_path):
            sub_directory = full_project_path / sub_directory_name
            if not sub_directory.is_dir():
                continue
            config_file_path = sub_directory / "config.py"
            if not config_file_path.is_file():
                continue
            configuration = import_module(
                f"{project_dir_name}.{sub_directory_name}.config"
            )
            configuration.title = title
            configuration.content_item_id = config_content_item_id
            yield configuration


def get_project_configuration(content_item_id, flavours):
    for configuration in get_all_marker_configs():
        if configuration.content_item_id != content_item_id:
            continue
        config_flavours = configuration.flavours
        if _flavours_match(config_flavours, flavours):
            return configuration


def mark_project(content_item_id, flavours, url=None, self_test=False, fail_fast=False):
    """This is the entrypoint, this function actually does the work of marking the code"""

    if not DOWNLOAD_DIR.exists():
        os.system(f"mkdir -p {DOWNLOAD_DIR}")

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
    steps = mark_project(content_item_id, flavours, url)
    print_steps_result(steps)
    print("----------------------------------------")
    print("REVIEW")
    print("----------------------------------------")
    print_final_review(steps)


def test_project_configuration(content_item_id, flavours):
    steps = mark_project(
        content_item_id=content_item_id,
        flavours=flavours,
        self_test=True,
        fail_fast=True,
    )
    print_steps_result(steps)


def print_final_review(steps):
    breakpoint()
    pass


def print_steps_result(steps):
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


# test_project_configuration(
#     content_item_id=705,
#     flavours=["python"],
# )

# test_project_configuration(
#     content_item_id=705,
#     flavours=["javascript"],
# )

# test_project_configuration(
#     content_item_id=223,
#     flavours=["javascript"],
# )

# test_project_configuration(
#     content_item_id=223,
#     flavours=["python"],
# )

# test_project_configuration(
#     content_item_id=223,
#     flavours=["java"],
# )


# test_project_configuration(
#     content_item_id=756,
#     flavours=["java"],
# )

# test_project_configuration(
#     content_item_id=756,
#     flavours=["javascript"],
# )

# test_project_configuration(
#     content_item_id=756,
#     flavours=["python"],
# )


# test_project_configuration(
#     content_item_id=186,
#     flavours=["javascript"],
# )


# test_project_configuration(
#     content_item_id=186,
#     flavours=["python"],
# )
