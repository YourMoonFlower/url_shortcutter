from ipware import get_client_ip


class RequestIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        request.client_ip = ip

        return self.get_response(request)
