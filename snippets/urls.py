from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from snippets.views import SnippetViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view


# setting up schema
schema_view = get_schema_view(title='Pastebin API')

# create router, register ViewSets with router
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# API urls now determined automatically by using a router
# Login / logout views for browsable API
urlpatterns = [
    url('^schema/$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
