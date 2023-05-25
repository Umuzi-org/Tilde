from core.models import Team, UserGroup, UserGroupMembership


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for group in UserGroup.objects.filter(active=True):
            print(group.name)
            # team, _ = Team.objects.get_or_create(name=group.name)
            # team.active = group.active
            # team.sponsor_organisation = group.sponsor_organisation
            # team.school_organisation = group.school_organisation
            # team.save()

            for membership in UserGroupMembership.objects.filter(
                group=group, permission_manage=True
            ):
                print(membership.user.email)

            print()
