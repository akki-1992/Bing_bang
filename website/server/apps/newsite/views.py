from django.shortcuts import render
import json
from numpy.random import rand
from rest_framework import views,status
from rest_framework.response import Response
from apps.ml.registry import MLRegistry
from server.wsgi import registry

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

class PredictView(views.APIView):
    def post(self, request, newsite_name, format=None):

        algorithm_status = self.request.query_params.get("status","production")
        algorithm_version = self.request.query_params.get("version")

        algs = MLAlgorithm.objects.filter(parent_newsite__name = newsite_name, status__status =algorithm_status,status__active=True)

        if algorithm_version is not None:
            algs = algs.filter(version = algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(algs) != 1 and algorithm_status != "ab_testing":
            return Response(
                {"status": "Error", "message": "ML algorithm selection is ambiguous. Please specify algorithm version."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1

        algorithm_object = registry.newsite[algs[alg_index].id]
        prediction = algorithm_object.compute_prediction(request.data)


        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlalgorithm=algs[alg_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)
# Create your views here.
