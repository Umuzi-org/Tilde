from core.models import UserGroup, User, UserGroupMembership


def get_student_users(who):
    if "@" in who:
        return [User.objects.get(email=who)]
    group = UserGroup.objects.get(name=who)
    return [
        o.user
        for o in UserGroupMembership.objects.filter(
            permission_student=True, group=group, user__active=True
        )
    ]