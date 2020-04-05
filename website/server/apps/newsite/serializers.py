from rest_framework import serializers
from apps.newsite.models import newsite
from apps.newsite.models import MLAlgorithm
from apps.newsite.models import MLAlgorithmStatus
from apps.newsite.models import MLRequest

class newsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = newsite
        read_only_fields = ("id","name","owner","created_at")
        fields = read_only_fields

class MLAlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self,mlalgorithm):
        return MLAlgorithmStatus.objects.filter(parent_mlalgorithm=mlalgorithm).latest('created_at').status
    class Meta:
        model = MLAlgorithm
        read_only_fields = ("id","name","description","code","version","owner","created_at","parent_newsite","current_status")
        fields = read_only_fields

class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        read_only_fields = ("id","active")
        fields = ("id","active","status","created_by","created_at","parent_mlalgorithm")

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_ony_fields = ("id",
                "input_data",
                "full_response",
                "response",
                "created_at",
                "parent_mlalgorithm",
                )
        fields = (
                "id",
                "input_data",
                "full_response",
                "response",
                "feedback",
                "created_at",
                "parent_mlalgorithm",)
        
