"""GET /healthz for SPARC Cloud's health check: 200 when the database answers, 503 when not.

It runs BEFORE every other middleware on purpose: Kubernetes calls it with the pod's IP address as the host name,
which ALLOWED_HOSTS (rightly) does not list."""
import logging

from django.db import connection
from django.http import HttpResponse

log = logging.getLogger(__name__)


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != "/healthz":
            return self.get_response(request)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception as e:  # noqa: BLE001
            log.warning("Health check: database not answering (%s)", e.__class__.__name__)
            return HttpResponse("database not answering", status=503, content_type="text/plain")
        return HttpResponse("ok", content_type="text/plain")
