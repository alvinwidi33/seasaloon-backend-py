import graphene
from graphene_django import DjangoObjectType
from .models import Treatment
from prescription.models import Prescription
from prescription.schema import PrescriptionType

class TreatmentType(DjangoObjectType):
    prescriptions = graphene.List(lambda: PrescriptionType)

    class Meta:
        model = Treatment
        fields = "__all__"

    def resolve_all_treatments(root, info):
        return Treatment.objects.prefetch_related("prescriptions__medicine").all()


class Query(graphene.ObjectType):
    all_treatments = graphene.List(TreatmentType)
    treatment_by_id = graphene.Field(TreatmentType, id=graphene.UUID(required=True))

    def resolve_all_treatments(root, info):
        return Treatment.objects.all()

    def resolve_treatment_by_id(root, info, id):
        return Treatment.objects.get(id=id)


schema = graphene.Schema(query=Query)