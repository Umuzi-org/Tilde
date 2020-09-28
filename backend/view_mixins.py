from rest_framework import authentication, permissions


class AuthMixin:
    """ this is applied to all views by default. Then if someone actualy needs permission then this mixin can be removed
    """

    # TODO: remove this. Just use defaults

    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAdminUser]
