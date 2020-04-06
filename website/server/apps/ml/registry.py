from apps.newsite.models import newsite
from apps.newsite.models import MLAlgorithm
from apps.newsite.models import MLAlgorithmStatus

class MLRegistry:
    def __init__(self):
        self.newsite = {}

    def add_algorithm(self,newsite_name,algorithm_object,algorithm_name,algorithm_status,algorithm_version,owner,algorithm_description,algorithm_code):
        newste, _ = newsite.objects.get_or_create(name=newsite_name,owner=owner)
        database_object, algorithm_created = MLAlgorithm.objects.get_or_create(name=algorithm_name,description=algorithm_description,code=algorithm_code,
                version=algorithm_version,
                owner=owner,
                parent_newsite=newste)
        if algorithm_created:
            status = MLAlgorithmStatus(status = algorithm_status,
                    created_by = owner,
                    parent_mlalgorithm = database_object,
                    active = True)
            status.save()
        self.newsite[database_object.id] = algorithm_object




