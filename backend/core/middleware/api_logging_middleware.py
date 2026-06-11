import time
import json
import logging

logger = logging.getLogger("api_logger")


class APILoggingMiddleware:
    """
    Middleware for logging all API requests with:
    - request metadata
    - response status
    - performance timing
    - error tracking
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        request_body = self._get_request_body(request)

        response = None
        error = None

        try:
            response = self.get_response(request)
        except Exception as e:
            error = str(e)
            raise

        duration_ms = round((time.time() - start_time) * 1000, 2)

        self._log_request(
            request=request,
            response=response,
            duration_ms=duration_ms,
            request_body=request_body,
            error=error,
        )

        return response

    def _get_request_body(self, request):
        """
        Safely extract JSON body (if present).
        Avoid breaking multipart/form-data or large payloads.
        """
        try:
            content_type = request.META.get("CONTENT_TYPE", "")

            if "application/json" in content_type:
                if request.body:
                    return json.loads(request.body.decode("utf-8"))
        except Exception:
            return "<unparsable body>"

        return None

    def _log_request(self, request, response, duration_ms, request_body, error):
        user = getattr(request, "user", None)

        log_data = {
            "method": request.method,
            "path": request.path,
            "user": str(user) if user and user.is_authenticated else "anonymous",
            "ip": self._get_client_ip(request),
            "status_code": getattr(response, "status_code", None),
            "duration_ms": duration_ms,
            "request_body": request_body,
            "error": error,
        }

        # Decide log level
        if error or (response and response.status_code >= 500):
            logger.error("API_ERROR", extra=log_data)

        elif response and response.status_code >= 400:
            logger.warning("API_WARNING", extra=log_data)

        elif duration_ms > 1000:
            logger.warning("SLOW_API", extra=log_data)

        else:
            logger.info("API_REQUEST", extra=log_data)

    def _get_client_ip(self, request):
        """
        Get real client IP (works behind proxies/load balancers)
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")