from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import PostViewSet, LikeViewSet, AnalyticsViewSet, bot_run

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('analytics/', AnalyticsViewSet.as_view(), name='analytics'),
    path('bot_run/', bot_run, name='bot_run'),
]
