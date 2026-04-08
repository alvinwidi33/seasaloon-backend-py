import graphene
from graphene_django import DjangoObjectType
from .models import Medicine

class MedicineType(DjangoObjectType):
    class Meta:
        model = Medicine
        fields = "__all__"

class Query(graphene.ObjectType):
    all_medicines = graphene.List(
        MedicineType,
        name=graphene.String(required=False),
        stock=graphene.Boolean(required=False),
        is_active=graphene.Boolean(required=False)
    )
    medicine_by_id = graphene.Field(
        MedicineType,
        id=graphene.UUID(required=True)
    )

    def resolve_all_medicines(root, info, name=None, stock=None, is_active=None):
        qs = Medicine.objects.all()

        if name:
            qs = qs.filter(name__icontains=name)

        if stock is True:
            qs = qs.filter(stock__lte=0)   
        elif stock is False:
            qs = qs.filter(stock__gt=0)    

        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        return qs

    def resolve_medicine_by_id(root, info, id):
        return Medicine.objects.get(id=id)
schema = graphene.Schema(query=Query)


class CreateMedicine(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        code = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=True)
        unit = graphene.String(required=True)
        description = graphene.String()

    medicine = graphene.Field(MedicineType)

    def mutate(self, info, name, code, price, stock, unit, description=None):
        medicine = Medicine.objects.create(
            name=name,
            code=code,
            price=price,
            stock=stock,
            unit=unit,
            description=description,
            is_active=True
        )
        return CreateMedicine(medicine=medicine)
    
class UpdateMedicine(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        price = graphene.Float()
        stock = graphene.Int()

    medicine = graphene.Field(MedicineType)

    def mutate(self, info, id, **kwargs):
        medicine = Medicine.objects.get(id=id)

        for key, value in kwargs.items():
            setattr(medicine, key, value)

        medicine.save()

        return UpdateMedicine(medicine=medicine)
    
class SoftDeleteMedicine(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    medicine = graphene.Field(MedicineType)

    def mutate(self, info, id):
        medicine = Medicine.objects.get(id=id)
        medicine.is_active = False
        medicine.save()
        return SoftDeleteMedicine(medicine=medicine)
    
class Mutation(graphene.ObjectType):
    create_medicine = CreateMedicine.Field()
    update_medicine = UpdateMedicine.Field()
    soft_delete_medicine = SoftDeleteMedicine.Field()