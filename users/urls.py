from django.urls import include, path
from rest_framework import routers

from users import views
from users.views import CustomUserRecordView


router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('customuser/', CustomUserRecordView.as_view()),
]
