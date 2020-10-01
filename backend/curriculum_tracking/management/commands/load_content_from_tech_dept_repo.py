from django.core.management.base import BaseCommand
from curriculum_tracking import models
import os
from curriculum_tracking import constants
from curriculum_tracking import helpers
import frontmatter
import re
import taggit
import requests
from typing import List, Dict
from pathlib import Path
import yaml
from curriculum_tracking import helpers


# these constants are keys in the hugo page frontmatter
TITLE = "title"
READY = "ready"
STORY_POINTS = "story_points"
TAGS = "tags"
TODO = "todo"

PREREQUISITES = "prerequisites"
HARD = "hard"
SOFT = "soft"

DB_ID = "_db_id"


def content_type_from_url(url):
    if "/projects/" in url:
        return models.ContentItem.PROJECT
    if "/topics/" in url:
        return models.ContentItem.TOPIC
    if "/workshops/" in url:
        return models.ContentItem.WORKSHOP
    raise Exception(f"cant find content type in url: {url}")


def _add_prerequisite(
    content_item: models.ContentItem, prerequisite: str, hard_requirement: bool
) -> models.ContentItemOrder:

    url = helpers.get_full_url_from_content_link_param(url_part=prerequisite)

    print(content_item)
    print(f"processing preprequisite: {prerequisite}")
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
    hard_prerequisites: List[str] = all_prerequisites.get(HARD, [])
    soft_prerequisites: List[str] = all_prerequisites.get(SOFT, [])

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


def set_available_flavours(
    content_item, raw_available_flavours, available_content_flavours
):
    right_hand_side = [i for l in available_content_flavours.values() for i in l]

    available_flavours = []
    for flavour in raw_available_flavours:
        if flavour in right_hand_side:
            available_flavours.append(flavour)
        else:
            available_flavours.extend(available_content_flavours[flavour])
    if (
        content_item.content_type == content_item.PROJECT
        and content_item.project_submission_type != content_item.NO_SUBMIT
    ):
        assert (
            available_flavours
        ), f"no available flavours specified. Be explicit. Perhaps you forgot to say available_flavours: ['none']\n\t{content_item.url}"

    if "none" in available_flavours:
        assert (
            len(available_flavours) == 1
        ), f"either it is None or it isnt!\n\t{content_item.url}"
        return  # nothing to do

    tags = [
        t[0]
        for t in [
            taggit.models.Tag.objects.get_or_create(name=tag_name)
            for tag_name in available_flavours
        ]
    ]

    for tag in tags:
        # if tag.lower() == "none":
        #     continue
        models.ContentAvailableFlavour.objects.get_or_create(
            tag=tag, content_item=content_item
        )
    # remove the unnecessary ones
    for tag in content_item.available_flavours.all():
        if tag not in tags:
            models.ContentAvailableFlavour.objects.get(
                tag=tag, content_item=content_item
            ).delete()

    final = sorted([o.name for o in content_item.available_flavours.all()])
    assert final == sorted(
        available_flavours
    ), f"Flavours dpnt match: Expected {available_flavours} but got {final}"


def save_content(file_path, content_type, repo_base_dir, available_content_flavours):
    print(f"processing {file_path}")

    content_item_post = frontmatter.load(file_path)
    meta = dict(content_item_post)
    assert meta["title"], f"{file_path} => {meta}"

    content_sub_dir = str(file_path).replace(str(repo_base_dir), "").strip("/")
    url = helpers.get_full_url_from_content_link_param(content_sub_dir)

    # assert requests.get(url).status_code != 404, f"{file_path} {content_type} => {url}"

    # actual_content_type = content_type
    # if (content_type == models.ContentItem.PROJECT) and meta.get(NO_FORM):
    #     actual_content_type = models.ContentItem.TOPIC
    reverse_content_types = {t[1]: t[0] for t in models.ContentItem.CONTENT_TYPES}
    reverse_submission_types = {
        t[1]: t[0] for t in models.ContentItem.PROJECT_SUBMISSION_TYPES
    }

    actual_content_type = (
        reverse_content_types[meta["content_type"]]
        if "content_type" in meta
        else content_type
    )

    project_submission_type = (
        reverse_submission_types[meta["submission_type"]]
        if "submission_type" in meta
        else None
    )

    assert actual_content_type, f"{file_path} {content_type} => {actual_content_type}"

    if "from_repo" in meta:
        try:
            continue_from_repo = models.ContentItem.objects.get(
                url=helpers.get_full_url_from_content_link_param(meta["from_repo"])
            )

            print(f"continue from existing content item: {continue_from_repo}")
            continue_from_repo = save_content(  # saving it anyway because there are new fields...
                file_path=repo_base_dir / "content" / meta["from_repo"] / "_index.md",
                content_type=models.ContentItem.PROJECT,
                repo_base_dir=repo_base_dir,
                available_content_flavours=available_content_flavours,
            )

        except models.ContentItem.DoesNotExist:

            continue_from_repo = save_content(
                file_path=repo_base_dir / "content" / meta["from_repo"] / "_index.md",
                content_type=models.ContentItem.PROJECT,
                repo_base_dir=repo_base_dir,
                available_content_flavours=available_content_flavours,
            )
            print(f"continue from new content item: {continue_from_repo}")
        assert continue_from_repo

    else:
        continue_from_repo = None

    defaults = {
        "content_type": actual_content_type,
        "title": meta["title"],
        "story_points": int(meta.get("story_points", 1)),
        "url": url,
        # "available_flavours": meta.get("available_flavours"),
        "topic_needs_review": meta.get("topic_needs_review", False),
        "project_submission_type": project_submission_type,
        "continue_from_repo": continue_from_repo,
        "template_repo": meta.get("template_repo"),
    }

    print(f"saving  {defaults['title']}")

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

    set_available_flavours(
        content_item, meta.get("available_flavours", []), available_content_flavours
    )

    # if (
    #     content_item.project_submission_type
    #     and content_item.project_submission_type != content_item.NO_SUBMIT
    # ):
    #     assert (
    #         content_item.available_flavours.count()
    #     ), f"{content_item} has no flavours!!"

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

    return content_item


def create_or_update_content(
    content_type, root_path, repo_base_dir, available_content_flavours
):

    for file_path in recurse_get_all_content_index_file_paths(root_path):
        assert file_path.name == "_index.md", f"Bad content name: {file_path}"

        save_content(
            file_path=file_path,
            content_type=content_type,
            repo_base_dir=repo_base_dir,
            available_content_flavours=available_content_flavours,
        )

    # assert root_path.is_dir(), root_path
    # for child in root_path.iterdir():
    #     if child.is_dir():
    #         create_or_update_content(
    #             content_type, child, repo_base_dir, available_content_flavours
    #         )
    #     else:
    #         name = child.name
    #         if name == "_index.md":
    #             save_content(
    #                 file_path=child,
    #                 content_type=content_type,
    #                 repo_base_dir=repo_base_dir,
    #                 available_content_flavours=available_content_flavours,
    #             )


def recurse_get_all_content_index_file_paths(root_path):

    assert root_path.is_dir(), root_path
    for child in root_path.iterdir():
        if child.is_dir():
            for path in recurse_get_all_content_index_file_paths(child):
                yield path
        else:
            name = child.name
            if name == "_index.md":
                yield child


def load_all_content_items_with_known_ids(root_path):
    seen_ids = {}
    contnent_paths = recurse_get_all_content_index_file_paths(root_path)
    available_content_flavours = _load_available_content_flavours(root_path)
    for file_path in contnent_paths:
        # if "angular-testing-cucumber" not in str(file_path):  # TODO
        #     continue
        content_item_post = frontmatter.load(file_path)
        if DB_ID not in content_item_post:
            continue

        db_id = content_item_post[DB_ID]

        assert (
            db_id not in seen_ids
        ), f"Same ID on two content items!!\n\tid={db_id}\n\t{seen_ids[db_id]}\n\t{file_path}"
        seen_ids[db_id] = file_path
        save_content(
            file_path,
            content_type=None,
            repo_base_dir=root_path,
            available_content_flavours=available_content_flavours,
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


def content_item_file_path(repo_base_dir, content_item):
    parts = content_item.url.split("/content/")
    assert len(parts) == 2, parts
    return repo_base_dir / "content" / parts[1]


def add_all_prereq(repo_base_dir):
    for content_item in models.ContentItem.objects.all():
        print(f"{content_item.id} {content_item}")

        file_path = content_item_file_path(repo_base_dir, content_item)
        print(file_path)
        meta = dict(frontmatter.load(file_path))

        _manage_prerequisites(meta, content_item)
        content_item.save()


def remove_missing_content_items_from_db(repo_base_dir):
    """if there is a content item in the database that doesnt exist in the content repo then delete it"""

    for content_item in models.ContentItem.objects.all():
        file_path = content_item_file_path(repo_base_dir, content_item)
        print(f"checking {file_path} exists")
        if not os.path.exists(file_path):
            print("deleting!")
            models.AgileCard.objects.filter(content_item=content_item).delete()
            models.ContentItemOrder.objects.filter(post=content_item).delete()
            models.ContentItemOrder.objects.filter(pre=content_item).delete()
            models.TopicProgress.objects.filter(content_item=content_item).delete()
            # models.RecruitProject.objects.filter(content_item=content_item).delete()
            content_item.delete()


def _load_available_content_flavours(repo_base_dir):
    full_path = repo_base_dir / "flavours.yaml"
    with open(full_path, "r") as f:
        return yaml.load(f)


def load_content_from_tech_dept_repo(repo_base_dir):
    available_content_flavours = _load_available_content_flavours(repo_base_dir)

    create_or_update_content(
        content_type=models.ContentItem.WORKSHOP,
        root_path=repo_base_dir / "content/workshops",
        repo_base_dir=repo_base_dir,
        available_content_flavours=available_content_flavours,
    )
    create_or_update_content(
        content_type=models.ContentItem.TOPIC,
        root_path=repo_base_dir / "content/topics",
        repo_base_dir=repo_base_dir,
        available_content_flavours=available_content_flavours,
    )
    create_or_update_content(
        content_type=models.ContentItem.PROJECT,
        root_path=repo_base_dir / "content/projects",
        repo_base_dir=repo_base_dir,
        available_content_flavours=available_content_flavours,
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
                    o.remove(flavour)

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
            url = helpers.get_full_url_from_content_link_param(params["path"])

            try:
                content_item = models.ContentItem.objects.get(url=url)
            except models.ContentItem.DoesNotExist:
                raise Exception(f"cannot find contentitem with url = {url}")

            flavours = [s.strip() for s in params.get("flavour", "").split(",") if s]
            available_flavour_names = content_item.available_flavour_names

            if "none" in available_flavour_names:
                assert (
                    len(available_flavour_names) == 1
                ), f"available_flavour_names = {available_flavour_names}. Either it's None or it isn't!\n\t{params['path']}"
            available_flavour_names = [
                s for s in available_flavour_names if s != "none"
            ]

            if available_flavour_names:
                assert (
                    flavours
                ), f"No flavours specfied, choose at least one of: {available_flavour_names}\n\t{line}"

            for flavour in flavours:
                assert (
                    flavour in available_flavour_names
                ), f"{flavour} not allowed in {url}, choose one of: {available_flavour_names}\n\tpath={params['path']}"

            if not content_item.id in seen_content_item_ids:
                # we haven't seen it before
                seen_content_item_ids.append(content_item.id)
                yield content_item, hard_requirement, flavours


def set_up_curriculums_from_tech_dept_repo(curriculums_base_dir):
    for curriculum in models.Curriculum.objects.all():
        print(f"Processing curriculum: {curriculum}")
        name = curriculum.short_name.lower().replace(" ", "-")
        # # TODO::::
        # if "django" not in name:
        #     continue
        file_path = curriculums_base_dir / f"{name}.md"
        set_up_single_curriculum_from_file(curriculum, file_path)


def validate_card_creation():
    """the proof is in the pudding. Can we make cards without any of the internal sanity checks failing"""
    for curriculum in models.Curriculum.objects.all():
        ordered_content_items = helpers.get_ordered_content_items(curriculum)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path_to_tech_dept_repo", type=str, nargs="?")

    def handle(self, *args, **options):
        path_to_repo = options.get("path_to_tech_dept_repo", "")
        if path_to_repo:
            repo_base_dir = Path(path_to_repo)
            curriculums_base_dir = repo_base_dir / "content/syllabuses"
        else:
            # we are working with the latest and greatest...
            download_latest_tech_dept_repo()
            repo_base_dir = constants.FULL_PATH
            curriculums_base_dir = constants.CURRICULUMS_BASE_DIR

        load_all_content_items_with_known_ids(repo_base_dir)
        remove_missing_content_items_from_db(repo_base_dir)
        load_content_from_tech_dept_repo(repo_base_dir)
        add_all_prereq(repo_base_dir)

        set_up_curriculums_from_tech_dept_repo(curriculums_base_dir)

        if not path_to_repo:
            # working locally, this might not actually exist yet
            check_content_urls_exist()


# TODO: BUG: optional syllabus content requirements are skipped over
