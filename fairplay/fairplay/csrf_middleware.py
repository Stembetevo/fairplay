"""
Custom CSRF middleware that exempts API endpoints from CSRF protection.
Since the frontend is a separate SPA accessing the API, we relax CSRF for /api/* endpoints.
"""
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.decorators import decorator_from_middleware


class APICSRFMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that exempts /api/ endpoints from CSRF protection.
    This allows cross-origin API requests from the Vite frontend without CSRF tokens.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exempt /api/ endpoints from CSRF protection by setting a marker
        if request.path.startswith('/api/'):
            # Mark request as exempt from CSRF
            request._dont_enforce_csrf_checks = True
            return None
        # Apply normal CSRF protection to other endpoints
        return super().process_view(request, view_func, view_args, view_kwargs)

