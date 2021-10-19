from django.urls import path
# from projects import views
from . import views
# from rest_framework.documentation import include_docs_urls
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from rest_framework import routers

# router = routers.DefaultRouter()
# router = routers.SimpleRouter()
# router.register(r'projects', views.ProjectViewSet)
# urlpatterns = [
#
# ]
# urlpatterns += router.urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('index1/',index),
    # path('index2/',index1),
    # path('',views.MyView.as_view()),
    path('', views.TestsuitsViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('<int:id>/run/', views.TestsuitsViewSet.as_view({
        'post': 'run'
    })),
    path('<int:id>/', views.TestsuitsViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update'
    })),
]