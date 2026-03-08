class AnonymousViewLimitMiddleware:

    MAX_VIEWS = 10

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated:
            request.session.setdefault("free_views_used", 0)

        response = self.get_response(request)

        return response