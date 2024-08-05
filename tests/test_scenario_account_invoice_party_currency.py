import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear, create_tax)
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.modules.currency.tests.tools import get_currency
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install account_invoice_party_currency
        activate_modules([
            'account_invoice_party_currency',
            'stock_supply',
            'sale',
            'purchase',
        ])

        # Create company
        currency = get_currency('USD')
        eur = get_currency('EUR')
        _ = create_company(currency=currency)
        company = get_company()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)

        # Create tax
        tax = create_tax(Decimal('.10'))
        tax.save()

        # Create party
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.second_currency = eur
        party.save()
        self.assertEqual(party.currency, currency)
        self.assertEqual(party.second_currency, eur)

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        Product = Model.get('product.product')
        product = Product()
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.list_price = Decimal('40')
        template.cost_price = Decimal('25')
        template.purchasable = True
        template.salable = True
        template.save()
        product.template = template
        product.save()

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create sale
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = party
        sale.click('quote')
        self.assertEqual(sale.currency, eur)
