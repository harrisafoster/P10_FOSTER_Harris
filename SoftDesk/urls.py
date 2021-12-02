"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from projects.views import ProjectViewSet, ContributorViewSet
from user_management.views import CreateUserView, PersonalTokenObtainView

router = ExtendedSimpleRouter()
(
    router.register(r'projects', ProjectViewSet, basename='projects')
          .register(r'contributors',
                    ContributorViewSet,
                    basename='contributors',
                    parents_query_lookups=['project'])
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', PersonalTokenObtainView.as_view(), name='token_obtain'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
