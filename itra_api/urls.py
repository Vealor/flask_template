from django.urls import include, path
from itra_api.api import views
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('hello', views.HelloView.as_view(), name='hello'),
    path('api/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify')
]
