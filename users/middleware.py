from django.utils import timezone

from users.models import CustomUser


class UpdateActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'User is not authenticated'
        if request.user.is_authenticated:
            CustomUser.objects.filter(user__id=request.user.id).update(last_activity=timezone.now())
