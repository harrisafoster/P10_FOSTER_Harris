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
from rest_framework_simplejwt.views import TokenObtainPairView

from projects.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
from user_management.views import CreateUserView

router = ExtendedSimpleRouter()
(
    router.register(r'projects', ProjectViewSet, basename='projects')
          .register(r'contributors',
                    ContributorViewSet,
                    basename='contributors',
                    parents_query_lookups=['project'])
)
(
    router.register(r'projects', ProjectViewSet, basename='projects')
          .register(r'issues',
                    IssueViewSet,
                    basename='issues',
                    parents_query_lookups=['project'])
          .register(r'comments',
                    CommentViewSet,
                    basename='comments',
                    parents_query_lookups=['project', 'issue'])
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
