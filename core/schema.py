import graphene

from medicine.schema import Query as MedicineQuery
from treatment.schema import Query as TreatmentQuery
from prescription.schema import Query as PrescriptionQuery


class Query(
    MedicineQuery,
    TreatmentQuery,
    PrescriptionQuery,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)