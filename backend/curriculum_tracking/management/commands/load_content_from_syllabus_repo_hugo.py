from factory import declarations
from core.models import Curriculum
from django.core.management.base import BaseCommand
from curriculum_tracking import models
import os
from curriculum_tracking import constants

import frontmatter
import re
import taggit
import requests
from typing import List, Dict
from pathlib import Path
import yaml
from curriculum_tracking import helpers

# these constants are keys in the hugo page frontmatter
STORY_POINTS = "story_points"

TITLE = "title"
READY = "ready"
STORY_POINTS = "story_points"
TAGS = "tags"
TODO = "todo"

PREREQUISITES = "prerequisites"
HARD = "hard"
SOFT = "soft"

DB_ID = "_db_id"


class Helper:
    content_items_seen_by_id: Dict[int, str] = {}

    @classmethod
    def get_full_url_from_partial(cls, part: str):
        part = str(part)
        part = part.strip("/")
        if part.endswith("_index.md"):
            part = part[: -len("/_index.md")]
        if part.startswith("content/"):
            part = part[len("content/") :]
        assert not part.endswith("index.md"), f"invalid url part: {part}"
        assert not part.startswith("content/"), f"invalid url part: {part}"

        return cls.url_template.format(url_part=part)

    @classmethod
    def set_url_template(cls, url_template: str):
        cls.url_template = url_template

    @classmethod
    def set_repo_base_dir(cls, repo_base_dir):
        cls.repo_base_dir = Path(repo_base_dir)

    @classmethod
    def process_available_learning_outcomes(cls):
        full_path = Helper.repo_base_dir / "learning_outcomes.yaml"

        if not full_path.exists():
            return

        with open(full_path, "r") as f:
            raw_learning_outcomes = yaml.load(f)

        outcome_names = list(raw_learning_outcomes.keys())
        assert len(outcome_names) == len(set(outcome_names)), "names must be unique"

        all_outcomes = []

        # first deal with the outcomes with ids
        for name, info in raw_learning_outcomes.items():
            if DB_ID in info and info[DB_ID]:
                defaults = {"name": name, "description": info["description"]}
                o, _ = models.LearningOutcome.get_or_create_or_update(
                    id=info[DB_ID], overrides=defaults, defaults=defaults
                )
                all_outcomes.append(o)

        # then the outcomes without ids
        for name, info in raw_learning_outcomes.items():
            if not info.get(DB_ID):
                defaults = {"name": name, "description": info["description"]}
                o = models.LearningOutcome.objects.create(
                    id=models.LearningOutcome.get_next_available_id(),
                    name=name,
                    description=info["description"],
                )
                all_outcomes.append(o)

        final_structure = {
            o.name: {"description": o.description, DB_ID: o.id} for o in all_outcomes
        }

        with open(full_path, "w") as f:
            yaml.dump(final_structure, f)

    @classmethod
    def load_available_content_flavours(cls):
        full_path = Helper.repo_base_dir / "flavours.yaml"
        with open(full_path, "r") as f:
            cls.available_content_flavours = yaml.load(f)

    @classmethod
    def save_content(cls, file_path):
        print(f"processing {file_path}")

        content_item_post = frontmatter.load(file_path)
        meta = dict(content_item_post)

        assert meta["title"], f"Title missing in frontmatter: {file_path} => {meta}"

        content_sub_dir = str(file_path).replace(str(cls.repo_base_dir), "").strip("/")
        # url = helpers.get_full_url_from_content_link_param(content_sub_dir)
        url = Helper.get_full_url_from_partial(content_sub_dir)
        # assert requests.get(url).status_code != 404, f"{file_path} {content_type} => {url}"

        # actual_content_type = content_type
        # if (content_type == models.ContentItem.PROJECT) and meta.get(NO_FORM):
        #     actual_content_type = models.ContentItem.TOPIC
        reverse_content_types = {t[1]: t[0] for t in models.ContentItem.CONTENT_TYPES}
        reverse_submission_types = {
            t[1]: t[0] for t in models.ContentItem.PROJECT_SUBMISSION_TYPES
        }

        actual_content_type = reverse_content_types[meta["content_type"]]

        project_submission_type = (
            reverse_submission_types[meta["submission_type"]]
            if "submission_type" in meta
            else None
        )

        if "from_repo" in meta:
            try:
                continue_from_repo = models.ContentItem.objects.get(
                    # url=helpers.get_full_url_from_content_link_param(meta["from_repo"])
                    url=Helper.get_full_url_from_partial(meta["from_repo"])
                )

                print(f"continue from existing content item: {continue_from_repo}")
                continue_from_repo = cls.save_content(  # saving it anyway because there are new fields...
                    file_path=cls.repo_base_dir
                    / "content"
                    / meta["from_repo"]
                    / "_index.md",
                )

            except models.ContentItem.DoesNotExist:

                continue_from_repo = cls.save_content(
                    file_path=cls.repo_base_dir
                    / "content"
                    / meta["from_repo"]
                    / "_index.md",
                )
                print(f"continue from new content item: {continue_from_repo}")
            assert continue_from_repo
            assert continue_from_repo.content_type == models.ContentItem.PROJECT

        else:
            continue_from_repo = None

        defaults = {
            "content_type": actual_content_type,
            "title": meta["title"],
            "story_points": int(meta.get("story_points", 1)),
            "url": url,
            # "flavours": meta.get("flavours"),
            "topic_needs_review": meta.get("topic_needs_review", False),
            "project_submission_type": project_submission_type,
            "continue_from_repo": continue_from_repo,
            "template_repo": meta.get("template_repo"),
        }

        print(f"saving {defaults['title']}")

        if DB_ID in meta:
            content_item, created = models.ContentItem.get_or_create_or_update(
                pk=meta[DB_ID], defaults=defaults, overrides=defaults
            )
        else:
            try:
                content_item = models.ContentItem.objects.get(url=url)
            except models.ContentItem.DoesNotExist:
                content_item = models.ContentItem.objects.create(
                    id=models.ContentItem.get_next_available_id(), url=url
                )
            content_item.update(**defaults)
            content_item.save()

        set_flavours(
            content_item,
            meta.get("flavours", []),
            cls.available_content_flavours,
        )

        set_learning_outcomes(content_item, meta.get("learning_outcomes", []))

        assert (
            content_item.title
        ), f"{content_item.id} {content_item} has no title (file_path={file_path} meta={meta})"
        assert (
            content_item.content_type
        ), f"{content_item.id} {content_item} has no content_type"

        _update_tags(meta, content_item)
        content_item.save()

        nice_content_type = dict(models.ContentItem.CONTENT_TYPES)[actual_content_type]

        print(f"saved {content_item.id}")
        content_item_post[DB_ID] = content_item.id
        content_item_post["content_type"] = nice_content_type

        with open(file_path, "wb") as f:
            frontmatter.dump(content_item_post, f)

        cls.content_items_seen_by_id[content_item.id] = content_item.url
        return content_item


def _add_prerequisite(
    content_item: models.ContentItem, prerequisite: str, hard_requirement: bool
) -> models.ContentItemOrder:

    url = Helper.get_full_url_from_partial(prerequisite)

    print(content_item)
    print(f"processing preprequisite: {prerequisite}")
    print(f"url = {url}")
    required_content_item = models.ContentItem.objects.get(
        url=url,  # defaults={"content_type": content_type_from_url(url)}
    )

    defaults = {"hard_requirement": hard_requirement}
    order, created = models.ContentItemOrder.objects.get_or_create(
        pre=required_content_item, post=content_item, defaults=defaults
    )
    if not created:
        order.update(**defaults)
        order.save()

    assert order.pre.content_type, f"{order.pre} has no content type!"
    assert order.post.content_type, f"{order.post} has no content type!"

    return order


def _manage_prerequisites(meta: Dict, content_item):
    all_prerequisites = meta.get(PREREQUISITES, {})
    if not all_prerequisites:
        return
    hard_prerequisites: List[str] = all_prerequisites.get(HARD, []) or []
    soft_prerequisites: List[str] = all_prerequisites.get(SOFT, []) or []

    mentioned = [
        _add_prerequisite(content_item, prerequisite, True)
        for prerequisite in hard_prerequisites
    ] + [
        _add_prerequisite(content_item, prerequisite, False)
        for prerequisite in soft_prerequisites
    ]

    # and prune the rest
    saved = models.ContentItemOrder.objects.filter(post=content_item)
    expected_ids = [o.id for o in mentioned]
    actual_ids = [o.id for o in saved]

    # all the new prerequisites should be in the db
    for i in expected_ids:
        assert i in actual_ids, f"expected content item {i} as prerequisite"

    # and if any old prerequisite is no longer mentioned then it should be removed
    for o in saved:
        if o.id not in expected_ids:
            o.delete()


def _update_tags(meta, content_item):
    todo_tag, _ = taggit.models.Tag.objects.get_or_create(name=TODO)
    ready = meta.get("ready", False)
    if ready:
        assert ready == True, f"{ready} {type(ready)}"
        content_item.tags.remove(todo_tag)
    else:
        content_item.tags.add(todo_tag)
    if meta.get(TODO):
        content_item.tags.add(todo_tag)

    for tag_str in meta.get(TAGS, []):
        tag, _ = taggit.models.Tag.objects.get_or_create(name=tag_str.lower())
        content_item.tags.add(tag)


def set_learning_outcomes(content_item, outcome_names):
    print(f"setting outcomes: {outcome_names}")
    outcomes = [models.LearningOutcome.objects.get(name=name) for name in outcome_names]
    content_item.learning_outcomes.set(outcomes)


def set_flavours(content_item, raw_flavours, available_content_flavours):
    right_hand_side = [i for l in available_content_flavours.values() for i in l]

    flavours = []
    for flavour in raw_flavours:
        if flavour in right_hand_side:
            flavours.append(flavour)
        else:
            flavours.extend(available_content_flavours[flavour])
    if (
        content_item.content_type == content_item.PROJECT
        and content_item.project_submission_type != content_item.NO_SUBMIT
    ):
        assert (
            flavours
        ), f"no available flavours specified. Be explicit. Perhaps you forgot to say flavours: ['none']\n\t{content_item.url}"

    if "none" in flavours:
        assert (
            len(flavours) == 1
        ), f"either it is None or it isnt!\n\t{content_item.url}"
        return  # nothing to do

    tags = [
        t[0]
        for t in [
            taggit.models.Tag.objects.get_or_create(name=tag_name)
            for tag_name in flavours
        ]
    ]

    for tag in tags:
        # if tag.lower() == "none":
        #     continue
        models.ContentAvailableFlavour.objects.get_or_create(
            tag=tag, content_item=content_item
        )
    # remove the unnecessary ones
    for tag in content_item.flavours.all():
        if tag not in tags:
            models.ContentAvailableFlavour.objects.get(
                tag=tag, content_item=content_item
            ).delete()

    final = sorted([o.name for o in content_item.flavours.all()])
    assert final == sorted(
        flavours
    ), f"Flavours dpnt match: Expected {flavours} but got {final}"


def recurse_get_all_content_index_file_paths(root_path=None):

    root_path = root_path or Helper.repo_base_dir
    assert root_path.is_dir(), root_path
    for child in root_path.iterdir():
        if child.is_dir():
            for path in recurse_get_all_content_index_file_paths(child):
                yield path
        else:
            name = child.name
            if name == "_index.md":
                yield child


def load_all_content_items_with_known_ids():
    seen_ids = {}
    content_paths = recurse_get_all_content_index_file_paths()
    for file_path in content_paths:
        content_item_post = frontmatter.load(file_path)
        if DB_ID not in content_item_post:
            continue

        db_id = content_item_post[DB_ID]

        assert (
            db_id not in seen_ids
        ), f"Same ID on two content items!!\n\tid={db_id}\n\t{seen_ids[db_id]}\n\t{file_path}"
        seen_ids[db_id] = file_path
        Helper.save_content(
            file_path,
        )


def download_latest_tech_dept_repo():
    os.makedirs(constants.CLONE_DESTINATION, exist_ok=True)

    cwd = os.getcwd()

    if constants.FULL_PATH.exists():
        os.chdir(constants.FULL_PATH)
        os.system("git checkout master")
        os.system("git pull")
    else:
        os.chdir(constants.CLONE_DESTINATION)
        os.system(f"git clone {constants.REPO_SSH_URL} {constants.REPO_NAME}")
    os.chdir(cwd)


# def content_item_file_path(repo_base_dir, content_item):
#     parts = content_item.url.split("/content/")
#     assert len(parts) == 2, parts
#     return repo_base_dir / "content" / parts[1]


def add_all_prereq():

    for file_path in recurse_get_all_content_index_file_paths():
        # for content_item in models.ContentItem.objects.all():
        print(f"processing file at:\n\t{file_path}")
        content_sub_dir = (
            str(file_path).replace(str(Helper.repo_base_dir), "").strip("/")
        )

        # file_path = content_item_file_path(repo_base_dir, content_item)
        meta = dict(frontmatter.load(file_path))
        url = Helper.get_full_url_from_partial(content_sub_dir)
        try:
            content_item = models.ContentItem.objects.get(url=url)
        except models.ContentItem.DoesNotExist:
            print(
                f"cant find content item with\n\tcontent_sub_dir = {content_sub_dir}\n\turl = {url}"
            )
            raise

        print(f"{content_item.id} {content_item}")

        _manage_prerequisites(meta, content_item)
        content_item.save()


def user_prompt(question: str) -> bool:
    """ Prompt the yes/no-*question* to the user. """
    from distutils.util import strtobool

    while True:
        user_input = input(question + " [y/n]: ").lower()
        try:
            return bool(strtobool(user_input))
        except ValueError:
            print("Please use y/n or yes/no.\n")


def remove_missing_content_items_from_db():
    """if there is a content item in the database that doesnt exist in the content repo then delete it"""
    return
    for content_item in models.ContentItem.objects.all():
        # file_path = content_item_file_path(repo_base_dir, content_item)
        # TODO: check base url
        if content_item.id not in Helper.content_items_seen_by_id and user_prompt(
            f"Delete {content_item}"
        ):

            # print(f"checking {file_path} exists")
            # if not os.path.exists(file_path):
            print("deleting!")
            models.AgileCard.objects.filter(content_item=content_item).delete()
            models.ContentItemOrder.objects.filter(post=content_item).delete()
            models.ContentItemOrder.objects.filter(pre=content_item).delete()
            models.TopicProgress.objects.filter(content_item=content_item).delete()
            # models.RecruitProject.objects.filter(content_item=content_item).delete()
            content_item.delete()


def load_all_content_items_with_unknown_ids():

    for file_path in recurse_get_all_content_index_file_paths():
        assert file_path.name == "_index.md", f"Bad content name: {file_path}"

        content_item_post = frontmatter.load(file_path)
        if DB_ID in content_item_post:
            continue

        Helper.save_content(
            file_path=file_path,
        )


def check_content_urls_exist():
    """go through all ContentItem urls and make sure there are no 404s. If there is a 404 then tag the content"""
    print("checking urls")
    four04_tag, _ = taggit.models.Tag.objects.get_or_create(name="404")

    total = len(models.ContentItem.objects.all())
    for i, item in enumerate(models.ContentItem.objects.all()):
        print(f"getting {i}/{total}: {item.url}")
        if requests.get(item.url).status_code == 404:
            item.tags.add(four04_tag)
        else:
            item.tags.remove(four04_tag)


def set_up_single_curriculum_from_file(curriculum, file_path):
    if not file_path.exists():
        print(f"curriculum not available at {file_path}. SKIPPING")
        return

    expected_ids = []
    print(f"processing: {file_path}")
    with open(file_path, "r") as f:
        for index, (content_item, hard_requirement, flavours) in enumerate(
            _get_ordered_curriculum_items_from_page(f)
        ):
            # print(f"{index} {content_item} {hard_requirement}")
            override = {"hard_requirement": hard_requirement, "order": index + 1}

            o, created = models.CurriculumContentRequirement.objects.get_or_create(
                content_item=content_item, curriculum=curriculum, defaults=override
            )
            if not created:
                o.update(**override)
                o.save()

            for flavour in flavours:
                o.flavours.add(flavour)
            for flavour in o.flavours.all():
                if flavour.name not in flavours:
                    o.flavours.remove(flavour)

            expected_ids.append(o.id)

    for o in curriculum.content_requirements.all():
        if o.id not in expected_ids:
            o.delete()


def _get_content_link_parameters(match):
    raw_parameters = [s.split("=") for s in match.strip().split()]
    # ['path="projects/ios-mobile/swift-and-more"','flavours="xxx"']
    return {t[0]: t[1].strip('"').strip("'") for t in raw_parameters}


def _get_ordered_curriculum_items_from_page(file_stream):
    # keep track of what we have seen so we dont return the same thing twice
    seen_content_item_ids = []

    for line in file_stream:
        matches = re.findall("{{%\s*contentlink (.*)%}}", line)
        for match in matches:
            assert (
                "contentlink" not in match
            ), f'malformed line "{line}". Do you have multiple content links on the same line?'

            params = _get_content_link_parameters(match)

            # l = [s.strip() for s in match.split('"') if s.strip()]
            # assert len(l) in [1, 2], f"malformed content link {match}"
            hard_requirement = bool(int(params.get("optional", 0)))
            # url = helpers.get_full_url_from_content_link_param(params["path"])
            url = Helper.get_full_url_from_partial(params["path"])

            try:
                content_item = models.ContentItem.objects.get(url=url)
            except models.ContentItem.DoesNotExist:
                raise Exception(f"cannot find contentitem with url = {url}")

            flavours = [s.strip() for s in params.get("flavour", "").split(",") if s]
            flavour_names = content_item.flavour_names

            if "none" in flavour_names:
                assert (
                    len(flavour_names) == 1
                ), f"flavour_names = {flavour_names}. Either it's None or it isn't!\n\t{params['path']}"
            flavour_names = [s for s in flavour_names if s != "none"]

            if flavour_names:
                assert (
                    flavours
                ), f"No flavours specfied, choose at least one of: {flavour_names}\n\t{line}"

            for flavour in flavours:
                assert (
                    flavour in flavour_names
                ), f"{flavour} not allowed in {url}, choose one of: {flavour_names}\n\tpath={params['path']}"

            if not content_item.id in seen_content_item_ids:
                # we haven't seen it before
                seen_content_item_ids.append(content_item.id)
                yield content_item, hard_requirement, flavours


def curriculum_file_paths(curriculums_base_dir):
    for child in curriculums_base_dir.iterdir():
        if child.is_dir():
            raise Exception(child)
        name = child.name
        if name.startswith("_"):
            continue
        if not name.endswith(".md"):
            continue
        print(child)
        yield child


def get_creation_args_from_curricum_frontmatter(syllabus_frontmatter):
    return {
        "name": syllabus_frontmatter["title"],
    }


def load_all_curriculums_with_known_ids(curriculums_base_dir):
    seen_ids = {}

    for file_path in curriculum_file_paths(curriculums_base_dir):
        syllabus_frontmatter = frontmatter.load(file_path)
        if DB_ID not in syllabus_frontmatter:
            # this one doesn't have a known id. So skip it
            continue
        db_id = syllabus_frontmatter[DB_ID]

        assert (
            db_id not in seen_ids
        ), f"Same ID on two content items!!\n\tid={db_id}\n\t{seen_ids[db_id]}\n\t{file_path}"
        seen_ids[db_id] = file_path

        defaults = get_creation_args_from_curricum_frontmatter(syllabus_frontmatter)

        print("======================")
        print(defaults)
        curriculum, _ = Curriculum.get_or_create_or_update(
            id=db_id, defaults=defaults, overrides=defaults
        )
        set_up_single_curriculum_from_file(curriculum, file_path)


def load_all_curriculums_with_unknown_ids(curriculums_base_dir):
    for file_path in curriculum_file_paths(curriculums_base_dir):
        syllabus_frontmatter = frontmatter.load(file_path)
        if DB_ID in syllabus_frontmatter:
            # this one already has an id. Skip it
            continue
        defaults = get_creation_args_from_curricum_frontmatter(syllabus_frontmatter)

        curriculum = Curriculum.objects.create(
            id=Curriculum.get_next_available_id(), **defaults
        )
        syllabus_frontmatter[DB_ID] = curriculum.id
        with open(file_path, "wb") as f:
            frontmatter.dump(syllabus_frontmatter, f)

        set_up_single_curriculum_from_file(curriculum, file_path)


def set_up_curriculums_from_tech_dept_repo(curriculums_base_dir, currculum_name):
    if currculum_name:
        raise NotImplemented
    load_all_curriculums_with_known_ids(curriculums_base_dir)
    load_all_curriculums_with_unknown_ids(curriculums_base_dir)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path_to_tech_dept_repo", type=str)
        parser.add_argument("process_content", type=int)
        parser.add_argument("process_curriculums", type=int)
        parser.add_argument("currculum_name", type=str, nargs="?")

    def handle(self, *args, **options):
        url_template = "http://syllabus.africacode.net/{url_part}/"  # TODO: get this from command line instead
        path_to_repo = options.get("path_to_tech_dept_repo", "")
        process_content = options["process_content"]
        process_curriculums = options["process_curriculums"]

        Helper.set_url_template(url_template)
        Helper.set_repo_base_dir(path_to_repo)
        Helper.load_available_content_flavours()
        Helper.process_available_learning_outcomes()

        curriculums_base_dir = Helper.repo_base_dir / "content/syllabuses"
        if process_content:
            print("Processing Content....")
            # first we make sure that if something has an id, it gets saved first
            # this is because we generate the next available id based on what is already in the db. This stops id conflicts
            load_all_content_items_with_known_ids()
            load_all_content_items_with_unknown_ids()

            # now that all the content is loaded up, we check what should be removed
            # remove_missing_content_items_from_db()

            # now all the content is right. Link things up
            add_all_prereq()

        if process_curriculums:
            print("Processing Curriculums....")
            set_up_curriculums_from_tech_dept_repo(
                curriculums_base_dir, options.get("currculum_name")
            )


# TODO: BUG: optional syllabus content requirements are skipped over
