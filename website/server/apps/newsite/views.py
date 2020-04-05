from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import mixins

from apps.newsite.models import newsite
from apps.newsite.serializers import newsiteSerializer

from apps.newsite.models import MLAlgorithm
from apps.newsite.serializers import MLAlgorithmSerializer

from apps.newsite.models import MLAlgorithmStatus
from apps.newsite.serializers import MLAlgorithmStatusSerializer

from apps.newsite.models import MLRequest
from apps.newsite.serializers import MLRequestSerializer

class newsiteViewSet(
        mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
        serializer_class = newsiteSerializer
        queryset = newsite.objects.all()

class MLAlgorithmViewSet(
        mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()

def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm = instance.parent_algorithm,created_at__lt=instance.created_at,active=True)

    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class MLAlgorithmStatusViewSet(
        mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()
    def perform_create(self,serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_other_statuses(instance)

        except Exception as e:
            raise APIException(str(e))
class MLRequestViewSet(
        mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet,mixins.UpdateModelMixin):

    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

# Create your views here.