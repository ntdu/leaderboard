
from django.urls import path, include
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .auth import views as auth_views
from .user import views as user_views

app_name = 'api'
router = DefaultRouter()


urlpatterns = [
    path('v1/users/', user_views.RegistrationAPIView.as_view(), name='registration'),
    path('v1/users/me/', user_views.UserDetailView.as_view(), name='user-detail'),

    path('v1/login/', auth_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/refresh/', auth_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/logout/', auth_views.LogoutBlacklistTokenUpdateView.as_view(), name='logout'),

]

urlpatterns += router.urls
