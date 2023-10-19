from long_running_request_utils import actor
import logging

logger = logging.getLogger(__name__)

TEN_MINUTES = 10 * 60 * 1000  # milliseconds


@actor(max_retries=5, min_backoff=TEN_MINUTES, max_backoff=TEN_MINUTES)
def automark_single_project(project_id):
    from curriculum_tracking.models import RecruitProject, AgileCard
    from .models import ContentItemAutoMarkerConfig
    from .utils import get_automark_result, add_review

    project = RecruitProject.objects.get(pk=project_id)

    try:
        card = project.agile_card
        if card.status != AgileCard.IN_REVIEW:
            logger.info(f"SKIPPING: Card is not in review. Card status = {card.status}")
            return
    except AgileCard.DoesNotExist:
        pass

    # check that we should automark it
    flavours = project.flavour_names
    configs = ContentItemAutoMarkerConfig.objects.filter(
        content_item=project.content_item
    )
    configs = [o for o in configs if o.flavours_match(flavours)]

    if len(configs) == 0:
        logger.info(
            f"SKIPPING: No matching automarker config instance. \n\tContentItem = {project.content_item} \n\tFlavours = {flavours}"
        )
        return

    assert (
        len(configs) == 1
    ), f"Too many matching automarker config instances. \n\tContentItem = {project.content_item} \n\tFlavours = {flavours}"

    config = configs[0]
    if config.mode != ContentItemAutoMarkerConfig.MODE_PROD:
        logger.info(
            f"SKIPPING: Automarker config instance is not in prod mode. \n\tContentItem = {project.content_item} \n\tFlavours = {flavours} \n\tMode = {config.mode}"
        )
        return

    logger.info(
        f"RUNNING: Project id = {project.id} \n\tContentItem = {project.content_item} \n\tFlavours = {flavours} \n\tMode = {config.mode}"
    )
    # at this point we know that the project should be automarked
    api_result = get_automark_result(
        link_submission=project.link_submission,
        repo_url=project.repository.ssh_url if project.repository else None,
        content_item_id=project.content_item_id,
        flavours=project.flavour_names,
    )

    logger.info(f"API result: {api_result}")

    add_review(project, api_result)
