from django.utils.timezone import now as current_time


def update_user_activity(self, user):
    if self.request.user.is_authenticated:
        user.objects.filter(user__id=self.request.user.id).update(last_activity=current_time())
