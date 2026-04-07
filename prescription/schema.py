import graphene
from graphene_django import DjangoObjectType
from .models import Prescription


class PrescriptionType(DjangoObjectType):
    class Meta:
        model = Prescription
        fields = "__all__"


class Query(graphene.ObjectType):
    all_prescriptions = graphene.List(PrescriptionType)
    prescription_by_id = graphene.Field(PrescriptionType, id=graphene.UUID(required=True))

    def resolve_all_prescriptions(root, info):
        return Prescription.objects.select_related("treatment", "medicine").all()

    def resolve_prescription_by_id(root, info, id):
        return Prescription.objects.get(id=id)


schema = graphene.Schema(query=Query)