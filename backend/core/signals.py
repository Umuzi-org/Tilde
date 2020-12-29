from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import pre_delete
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission
from . import models
from django.dispatch import receiver

@receiver([pre_delete], sender=models.Team)
def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
    """Remove orphan permissions. See https://django-guardian.readthedocs.io/en/stable/userguide/caveats.html for details"""
    filters = Q(content_type=ContentType.objects.get_for_model(instance),
        object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()

