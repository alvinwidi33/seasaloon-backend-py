import graphene
from graphene_django import DjangoObjectType
from .models import Medicine

class MedicineType(DjangoObjectType):
    class Meta:
        model = Medicine
        fields = "__all__"

class Query(graphene.ObjectType):
    all_medicines = graphene.List(MedicineType)
    medicine_by_id = graphene.Field(MedicineType, id=graphene.UUID(required=True))

    def resolve_all_medicines(root, info):
        return Medicine.objects.all()

    def resolve_medicine_by_id(root, info, id):
        return Medicine.objects.get(id=id)

schema = graphene.Schema(query=Query)