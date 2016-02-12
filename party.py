#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Party', 'Invoice', 'Sale', 'Purchase', 'PurchaseRequest']
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'

    currency = fields.Many2One('currency.currency', 'Currency')


class CurrencyMixin:

    @fields.depends('party')
    def on_change_party(self):
        super(CurrencyMixin, self).on_change_party()
        if self.party and self.party.currency:
            self.currency = self.party.currency

    @classmethod
    def create(cls, vlist):
        pool = Pool()
        Party = pool.get('party.party')
        for values in vlist:
            if values.get('party') and not values.get('currency'):
                party = Party(values.get('party'))
                if party.currency:
                    values['currency'] = party.currency.id
        return super(CurrencyMixin, cls).create(vlist)


class Invoice(CurrencyMixin):
    __name__ = 'account.invoice'


class Sale(CurrencyMixin):
    __name__ = 'sale.sale'


class Purchase(CurrencyMixin):
    __name__ = 'purchase.purchase'


class PurchaseRequest:
    __name__ = 'purchase.request'

    @property
    def currency(self):
        if self.party and self.party.currency:
            return self.party.currency
        return super(PurchaseRequest, self).currency
