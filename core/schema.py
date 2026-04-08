import graphene

from medicine.schema import Query as MedicineQuery
from medicine.schema import Mutation as MedicineMutation

from treatment.schema import Query as TreatmentQuery
from treatment.schema import Mutation as TreatmentMutation

from invoice.schema import Query as InvoiceQuery
from invoice.schema import Mutation as InvoiceMutation


class Query(
    MedicineQuery,
    TreatmentQuery,
    InvoiceQuery,
    graphene.ObjectType,
):
    pass


class Mutation(
    MedicineMutation,
    TreatmentMutation,
    InvoiceMutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)