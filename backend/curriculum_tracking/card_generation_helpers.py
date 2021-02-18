from curriculum_tracking import models, helpers

from collections import namedtuple


class FlavourProgressMismatchError(TypeError):
    """there is a card with some flavour, and a progress item with no flavour at all"""

    def __init__(self, card, unflavoured_progress):
        message = f"{self.__doc__}\ncard = {card}\nunflavoured_progress = {unflavoured_progress}"
        super(FlavourProgressMismatchError, self).__init__(message)


_CurriculumContentItemOrdering = namedtuple(
    "_CurriculumContentItemOrdering",
    "content_item, is_hard_milestone, is_soft_milestone, flavours",
)


def _flavour_subset(content_item, specified_flavours):
    """The content item has some available flavours, eg: ts and js and python, the specified flavours is the specific flavour requested by the syllabus. Eg eg if python is requested then that's allowed. Basically we want an intersection"""

    subset = [o for o in specified_flavours if o in content_item.flavours.all()]
    return subset


def get_ordered_content_items(curriculum):
    content_requirements = models.CurriculumContentRequirement.objects.filter(
        curriculum=curriculum
    ).order_by("order")
    return list(
        _recurse_generate_ordered_content_items(
            content_requirements,
        )
    )


def _recurse_generate_ordered_content_items(content_requirements):
    # already_yielded_content_items = []
    yielded = []

    def _already_yielded(content_item_ordering):
        match = [
            o for o in yielded if o.content_item == content_item_ordering.content_item
        ]
        match = [
            o
            for o in match
            if sorted([tag.name for tag in o.flavours])
            == sorted([tag.name for tag in content_item_ordering.flavours])
        ]
        assert len(match) in [0, 1]
        return bool(match)

    for o in content_requirements:
        content_item = o.content_item
        flavours = o.flavours.all()

        required_content_order_data = _CurriculumContentItemOrdering(
            content_item,
            o.hard_requirement,
            not o.hard_requirement,
            _flavour_subset(content_item, flavours),
        )

        if _already_yielded(required_content_order_data):
            continue

        yielded.append(required_content_order_data)

        # if content_item in already_yielded_content_items:
        #     continue

        # already_yielded_content_items.append(content_item)
        all_required_items = _explode_content_item_requirements(
            content_item,
        )

        for required_item in all_required_items:
            # if required_item in already_yielded_content_items:
            #     continue

            prereq_content_order_data = _CurriculumContentItemOrdering(
                required_item, False, False, _flavour_subset(required_item, flavours)
            )
            if _already_yielded(prereq_content_order_data):
                continue
            yield prereq_content_order_data
            yielded.append(prereq_content_order_data)
            # already_yielded_content_items.append(required_item)

        yield required_content_order_data


def _explode_content_item_requirements(content_item, visited=None):
    visited = visited or []

    if content_item in visited:
        return

    visited.append(content_item)
    for o in content_item.all_prerequisite_content_items():
        for oo in _explode_content_item_requirements(o, visited):
            yield oo
        yield o


def general_update_card_progress(
    card_queryset,
    get_unfiltered_progress,
    progress_to_status,
    user,
    assign_card_progress_one_to_one,
):

    for card in card_queryset:

        all_progress = get_unfiltered_progress(card, user)

        flavours = sorted([o.name for o in card.flavours.all()])

        if len(flavours):
            unflavoured_progress = [o for o in all_progress if o.flavours.count() == 0]
            if len(unflavoured_progress):
                raise FlavourProgressMismatchError(card, unflavoured_progress)

        filtered_progress = [
            o
            for o in all_progress
            if sorted([o.name for o in o.flavours.all()]) == flavours
        ]

        if len(filtered_progress) > 1:
            breakpoint()
        assert len(filtered_progress) in [0, 1], filtered_progress

        if filtered_progress:
            progress = filtered_progress[0]

            assign_card_progress_one_to_one(card, progress)
            card.status = progress_to_status(card, progress)
        else:
            card.status = card.status_ready_or_blocked()

        card.save()


def _get_next_card_order(user):
    last = (
        models.AgileCard.objects.filter(assignees__in=[user]).order_by("order").last()
    )
    if last == None:
        return 1
    else:
        return last.order + 1


def generate_all_content_cards_for_user(user, curriculum=None):
    start_order = 0
    for course_reg in (
        user.course_registrations.order_by("order")
        .filter(active=True)
        .filter(suppress_card_generation=False)
    ):
        if curriculum:
            start_order = _get_next_card_order(user)
            if course_reg.curriculum != curriculum:
                continue

        print(f"processing: {course_reg.curriculum}")
        ordered_content_items = get_ordered_content_items(course_reg.curriculum)
        start_order = create_or_update_content_cards_for_user(
            user, ordered_content_items, start_order
        )


def update_topic_card_progress(user):
    card_queryset = models.AgileCard.objects.filter(
        assignees__in=[user], content_item__content_type=models.ContentItem.TOPIC
    )
    get_unfiltered_progress = lambda card, user: models.TopicProgress.objects.filter(
        content_item=card.content_item, user=user
    )

    def progress_to_status(card, progress):
        helpers.update_card_from_topic_progress(card, progress)
        return card.status

    def assign_card_progress_one_to_one(card, progress):
        assert card.topic_progress in [progress, None]
        card.topic_progress = progress

    general_update_card_progress(
        card_queryset,
        get_unfiltered_progress,
        progress_to_status,
        user,
        assign_card_progress_one_to_one,
    )


def update_workshop_card_progress(user):
    card_queryset = models.AgileCard.objects.filter(
        assignees__in=[user], content_item__content_type=models.ContentItem.WORKSHOP
    )

    get_unfiltered_progress = (
        lambda card, user: models.WorkshopAttendance.objects.filter(
            content_item=card.content_item, attendee_user=user
        )
    )

    progress_to_status = lambda *args: models.AgileCard.COMPLETE

    def assign_card_progress_one_to_one(card, progress):
        assert card.workshop_attendance in [progress, None]
        card.workshop_attendance = progress

    general_update_card_progress(
        card_queryset,
        get_unfiltered_progress,
        progress_to_status,
        user,
        assign_card_progress_one_to_one,
    )


def update_project_card_progress(user):

    card_queryset = models.AgileCard.objects.filter(
        assignees__in=[user], content_item__content_type=models.ContentItem.PROJECT
    )

    get_unfiltered_progress = lambda card, user: models.RecruitProject.objects.filter(
        content_item=card.content_item, recruit_users__in=[user]
    )

    def assign_card_progress_one_to_one(card, progress):
        assert card.recruit_project in [
            progress,
            None,
        ], f"{card.recruit_project} NOT in [{progress}, None]"

        # if progress.recruit_users.count() > 1:
        # _merge_cards(card, progress.flavours, progress.recruit_users)

        card.recruit_project = progress

    def progress_to_status(card, progress):
        helpers.update_card_from_project(card, progress)
        return card.status

    general_update_card_progress(
        card_queryset,
        get_unfiltered_progress,
        progress_to_status,
        user,
        assign_card_progress_one_to_one,
    )


def update_cards_accorrding_to_progress(user):
    update_topic_card_progress(user)
    update_project_card_progress(user)
    update_workshop_card_progress(user)


def generate_all_content_cards_for_team(team):
    todo


def generate_and_update_all_cards_for_user(user, curricullum):
    generate_all_content_cards_for_user(user, curricullum)
    update_cards_accorrding_to_progress(user)


def _get_or_create_or_update_card(
    user,
    content_item,
    defaults,
    overrides,
    flavours,
):

    cards = models.AgileCard.objects.filter(
        assignees__in=[user],
        content_item=content_item,
    )

    matching_card = None

    for card in cards:
        if card.flavours_match([o.name for o in flavours]):
            matching_card = card
            break

    if matching_card:
        matching_card.update(**overrides)
        return matching_card

    # no matching card, make one
    card = models.AgileCard.objects.create(
        content_item=content_item,
        **defaults,
    )
    card.update(**overrides)
    card.set_flavours(flavours)
    card.assignees.add(user)
    return card


def create_or_update_content_cards_for_user(user, ordered_content_items, start_order=0):
    completed_cards = []
    order = start_order

    for (
        index,
        (content_item, is_hard_milestone, is_soft_milestone, flavours),
    ) in enumerate(ordered_content_items):

        if content_item.project_submission_type == content_item.NO_SUBMIT:
            continue
            # TODO: this is inelligant. If a NOSUBMIT project is here then what should that mean

        order = start_order + index
        hard_prereqesites = list(content_item.hard_prerequisite_content_items())

        requires_cards = []

        for required_item in hard_prereqesites:
            # since the cards are dealt with in order, the prerequisites already exist as
            # cards in the database

            prereq = models.AgileCard.objects.filter(
                assignees__in=[user], content_item=required_item
            )
            if len(prereq) == 0:
                pass
            elif len(prereq) == 1:
                requires_cards.append(prereq.get())
            else:
                # only a pre-req if the flavours match
                exact_flavour_match = [
                    o for o in prereq if o.flavours_match([o.name for o in flavours])
                ]
                if len(exact_flavour_match) == 1:
                    requires_cards.append(exact_flavour_match[0])
                elif len(exact_flavour_match) == 0:
                    print("TODO!!!!!!!!!!")
                    print("FIX!!!!!!!!!!")
                else:
                    breakpoint()
                    requires_cards.extend(exact_flavour_match)

                    pass

        blocked_by_cards = [
            o for o in requires_cards if o.status != models.AgileCard.COMPLETE
        ]

        # nothing can ever be blocked by a workshop
        blocked_by_cards = [
            o
            for o in blocked_by_cards
            if o.content_item.content_type != models.ContentItem.WORKSHOP
        ]

        if blocked_by_cards:
            default_status = models.AgileCard.BLOCKED
        else:
            default_status = models.AgileCard.READY

        print(f"Creating/updating card for {user} {content_item} {flavours}")

        # if (
        #     models.AgileCard.objects.filter(
        #         assignees__in=[user], content_item=content_item
        #     ).count()
        #     > 1
        # ):
        #     cards = models.AgileCard.objects.filter(
        #         assignees__in=[user], content_item=content_item
        #     )

        card = _get_or_create_or_update_card(
            user=user,
            content_item=content_item,
            defaults={
                "status": default_status,
                "order": order,
                "is_hard_milestone": is_hard_milestone,
                "is_soft_milestone": is_soft_milestone,
            },
            overrides={
                "is_hard_milestone": is_hard_milestone,
                "is_soft_milestone": is_soft_milestone,
                "order": order,  # we decide the order of the cards
                # "requires_cards": requires_cards,  # TODO: fill this in. On ui it would be good to have a list of ids
                # is_hard_requirement # TODO: fill this in. Eg if this is a hard prereq of a soft requirement then False
            },
            flavours=flavours,
        )

        card.requires_cards.set(requires_cards)
        card.set_flavours(flavours)
        assert card.flavours_match(
            [o.name for o in flavours]
        ), f"{card.flavours.all()} != {flavours}"

        if card.status == models.AgileCard.COMPLETE:
            completed_cards.append(card)

        if (
            card.status in [models.AgileCard.BLOCKED, models.AgileCard.READY]
        ) and card.status != default_status:
            card.status = default_status

        card.save()

        # print("+++++")
        # print(f"created = {created}\ncard = {card}")
    return order + 1
