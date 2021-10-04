# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Party', 'Invoice', 'Sale', 'Purchase', 'PurchaseRequest']


class CurrencyMixin(object):
    __slots__ = ()

    @fields.depends('party')
    def on_change_party(self):
        super(CurrencyMixin, self).on_change_party()
        if self.party and self.party.second_currency:
            self.currency = self.party.second_currency

    @classmethod
    def create(cls, vlist):
        pool = Pool()
        Party = pool.get('party.party')
        for values in vlist:
            if values.get('party') and not values.get('currency'):
                party = Party(values.get('party'))
                if party.second_currency:
                    values['currency'] = party.second_currency.id
        return super(CurrencyMixin, cls).create(vlist)


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    second_currency = fields.Many2One('currency.currency', 'Second Currency')

    @classmethod
    def __register__(cls, module_name):
        table = cls.__table_handler__(module_name)

        # Migration from 6.2: rename currency into second_currency
        if (table.column_exist('currency')
                and not table.column_exist('second_currency')):
            table.column_rename('currency', 'second_currency')

        super(Party, cls).__register__(module_name)


class Invoice(CurrencyMixin, metaclass=PoolMeta):
    __name__ = 'account.invoice'


class Sale(CurrencyMixin, metaclass=PoolMeta):
    __name__ = 'sale.sale'


class Purchase(CurrencyMixin, metaclass=PoolMeta):
    __name__ = 'purchase.purchase'


class PurchaseRequest(metaclass=PoolMeta):
    __name__ = 'purchase.request'

    @property
    def currency(self):
        # XXX: may break purchase_requisition
        if self.party and self.party.second_currency:
            return self.party.second_currency
        return super(PurchaseRequest, self).currency
