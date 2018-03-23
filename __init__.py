# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party


def register():
    Pool.register(
        party.Party,
        party.Invoice,
        party.Sale,
        module='account_invoice_party_currency', type_='model')
    Pool.register(
        party.Purchase,
        depends=['purchase'],
        module='account_invoice_party_currency', type_='model')
    Pool.register(
        party.PurchaseRequest,
        depends=['purchase_request'],
        module='account_invoice_party_currency', type_='model')
