"""hcjProject URL Configuration

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
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

scheme_view = get_schema_view(
    openapi.Info(
        title='hcj测试平台接口文档平台',
        default_version='V1',
        description='这是一个非常nice的接口文档',
        terms_of_service='',
        contact=openapi.Contact(email='531405546@qq.com'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('api/', include('rest_framework.urls')),
    path('users/', include('users.urls')),
    # re_path('^projects/$', include('projects.urls')),
    path('docs/', include_docs_urls(title='测试平台接口文档')),
    path('swagger/', scheme_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]