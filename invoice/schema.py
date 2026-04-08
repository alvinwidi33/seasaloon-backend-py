import graphene
from graphene_django import DjangoObjectType
from .models import Invoice, InvoiceItem


class InvoiceItemType(DjangoObjectType):
    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceType(DjangoObjectType):
    items = graphene.List(InvoiceItemType)

    class Meta:
        model = Invoice
        fields = "__all__"

    def resolve_items(self, info):
        return self.items.filter(is_active=True)

class Query(graphene.ObjectType):
    all_invoices = graphene.List(InvoiceType)
    invoice_by_id = graphene.Field(
        InvoiceType,
        id=graphene.UUID(required=True)
    )

    def resolve_all_invoices(root, info):
        return Invoice.objects.filter(is_active=True)

    def resolve_invoice_by_id(root, info, id):
        return Invoice.objects.get(id=id, is_active=True)

class CreateInvoice(graphene.Mutation):
    class Arguments:
        reservation_id = graphene.UUID(required=True)

    invoice = graphene.Field(InvoiceType)

    def mutate(self, info, reservation_id):
        invoice = Invoice.objects.create(
            reservation_id=reservation_id
        )
        return CreateInvoice(invoice=invoice)

class UpdateInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        total_price = graphene.Float()

    invoice = graphene.Field(InvoiceType)

    def mutate(self, info, id, **kwargs):
        invoice = Invoice.objects.get(id=id)

        for key, value in kwargs.items():
            setattr(invoice, key, value)

        invoice.save()

        return UpdateInvoice(invoice=invoice)

class SoftDeleteInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    invoice = graphene.Field(InvoiceType)

    def mutate(self, info, id):
        invoice = Invoice.objects.get(id=id)
        invoice.is_active = False
        invoice.save()

        return SoftDeleteInvoice(invoice=invoice)

class CreateInvoiceItem(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.UUID(required=True)
        treatment_id = graphene.UUID()
        medicine_id = graphene.UUID()
        quantity = graphene.Int()
        price = graphene.Float(required=True)

    item = graphene.Field(InvoiceItemType)

    def mutate(
        self,
        info,
        invoice_id,
        price,
        treatment_id=None,
        medicine_id=None,
        quantity=1
    ):
        item = InvoiceItem.objects.create(
            invoice_id=invoice_id,
            treatment_id=treatment_id,
            medicine_id=medicine_id,
            quantity=quantity,
            price=price
        )

        return CreateInvoiceItem(item=item)

class UpdateInvoiceItem(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        quantity = graphene.Int()
        price = graphene.Float()

    item = graphene.Field(InvoiceItemType)

    def mutate(self, info, id, **kwargs):
        item = InvoiceItem.objects.get(id=id)

        for key, value in kwargs.items():
            setattr(item, key, value)

        item.save()

        return UpdateInvoiceItem(item=item)

class SoftDeleteInvoiceItem(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    item = graphene.Field(InvoiceItemType)

    def mutate(self, info, id):
        item = InvoiceItem.objects.get(id=id)
        item.is_active = False
        item.save()

        return SoftDeleteInvoiceItem(item=item)

class Mutation(graphene.ObjectType):
    create_invoice = CreateInvoice.Field()
    update_invoice = UpdateInvoice.Field()
    soft_delete_invoice = SoftDeleteInvoice.Field()

    create_invoice_item = CreateInvoiceItem.Field()
    update_invoice_item = UpdateInvoiceItem.Field()
    soft_delete_invoice_item = SoftDeleteInvoiceItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)