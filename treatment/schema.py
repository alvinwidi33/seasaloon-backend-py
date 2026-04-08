import graphene
from graphene_django import DjangoObjectType
from .models import Treatment

class TreatmentType(DjangoObjectType):
    class Meta:
        model = Treatment
        fields = "__all__"


class Query(graphene.ObjectType):
    all_treatments = graphene.List(
        TreatmentType,
        name=graphene.String(required=False),
        is_active=graphene.Boolean(required=False)
    )

    treatment_by_id = graphene.Field(
        TreatmentType,
        id=graphene.UUID(required=True)
    )

    def resolve_all_treatments(root, info, name=None, is_active=None):
        qs = Treatment.objects.all()

        if name:
            qs = qs.filter(name__icontains=name)

        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        return qs

    def resolve_treatment_by_id(root, info, id):
        return Treatment.objects.get(id=id)


class CreateTreatment(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Float(required=True)

    treatment = graphene.Field(TreatmentType)

    def mutate(self, info, name, price, description=None):
        treatment = Treatment.objects.create(
            name=name,
            description=description,
            price=price,
            is_active=True
        )

        return CreateTreatment(treatment=treatment)



class UpdateTreatment(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()

    treatment = graphene.Field(TreatmentType)

    def mutate(self, info, id, **kwargs):
        treatment = Treatment.objects.get(id=id)

        for key, value in kwargs.items():
            setattr(treatment, key, value)

        treatment.save()

        return UpdateTreatment(treatment=treatment)



class SoftDeleteTreatment(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    treatment = graphene.Field(TreatmentType)

    def mutate(self, info, id):
        treatment = Treatment.objects.get(id=id)
        treatment.is_active = False
        treatment.save()

        return SoftDeleteTreatment(treatment=treatment)


# =====================
# MUTATION ROOT
# =====================
class Mutation(graphene.ObjectType):
    create_treatment = CreateTreatment.Field()
    update_treatment = UpdateTreatment.Field()
    soft_delete_treatment = SoftDeleteTreatment.Field()