# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party


def register():
    Pool.register(
        party.Party,
        party.Invoice,
        party.Sale,
        party.Purchase,
        party.PurchaseRequest,
        module='account_invoice_party_currency', type_='model')
