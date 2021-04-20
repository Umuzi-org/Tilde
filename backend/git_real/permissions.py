from rest_framework.permissions import BasePermission
import hmac
from hashlib import sha256
import hashlib
from backend.settings import GIT_REAL_WEBHOOK_SECRET


class IsWebhookSignatureOk(BasePermission):
    """
    see https://docs.github.com/en/developers/webhooks-and-events/securing-your-webhooks
    Code based on https://github.com/bloomberg/python-github-webhook/blob/master/github_webhook/webhook.py
    """

    def has_permission(self, request, view):
        body = request._request.body
        recieved_digest = request.headers.get("X-Hub-Signature")
        if not recieved_digest:
            return False
        digest = hmac.new(
            str.encode(GIT_REAL_WEBHOOK_SECRET, "utf-8"), body, hashlib.sha1
        ).hexdigest()
        correct = recieved_digest == "sha1=" + digest
        if not correct:
            breakpoint()

        return correct