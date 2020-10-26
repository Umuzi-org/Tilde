from core.models import UserGroup, User, UserGroupMembership


def get_users(who, filter_by_permission_student=False):
    if "@" in who:
        return [User.objects.get(email=who)]
    group = UserGroup.objects.get(name=who)
    memberships = UserGroupMembership.objects.filter(group=group, user__active=True)
    if filter_by_permission_student:
        memberships = memberships.filter(permission_student=True)
    return [o.user for o in memberships]


def get_student_users(who):
    return get_users(filter_by_permission_student=True)
