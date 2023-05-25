from rest_framework.filters import BaseFilterBackend


def ObjectPermissionsFilter(permission):
    class _ObjectPermissionsFilter(BaseFilterBackend):
        """
        A filter backend that limits results to those where the requesting user has the correct object level permissions.

        This is based heavily on https://github.com/rpkilby/django-rest-framework-guardian/blob/master/src/rest_framework_guardian/filters.py

        """

        perm_format = "%(app_label)s.view_%(model_name)s"
        shortcut_kwargs = {"accept_global_perms": True, "any_perm": True}

        def filter_queryset(self, request, queryset, view):

            from guardian.shortcuts import get_objects_for_user

            user = request.user
            if user.is_superuser:
                return queryset
            # if user.is_staff:
            #     return queryset

            # permission = self.perm_format % {
            #     'app_label': queryset.model._meta.app_label,
            #     'model_name': queryset.model._meta.model_name,
            # }
            # permission=["MOVE_CARDS","VIEW_ALL"]

            return get_objects_for_user(
                user, permission, queryset, **self.shortcut_kwargs
            )

    return _ObjectPermissionsFilter