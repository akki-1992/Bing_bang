from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.newsite.views import newsiteViewSet
from apps.newsite.views import MLAlgorithmViewSet
from apps.newsite.views import MLAlgorithmStatusViewSet
from apps.newsite.views import MLRequestViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"newsite", newsiteViewSet, basename="newsite")
router.register(r"mlalgorithms", MLAlgorithmViewSet, basename="mlalgorithms")
router.register(r"mlalgorithmstatuses", MLAlgorithmStatusViewSet, basename="mlalgorithmstatuses")
router.register(r"mlrequests", MLRequestViewSet, basename="mlrequests")

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
]
