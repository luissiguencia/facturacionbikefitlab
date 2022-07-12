# -*- coding: utf-8 -*-
{
    'name': "Ecuador - Invoicing Basic",
    'summary': """
        Ecuadorian Basic Invocing
        """,

    'description': """
Localización Ecuatoriana OpenAlliance.
============================================

Author: OpenAlliance Cía. Ltda.
        https://www.openalliance-la.com

Description:

Minimum tax prerequisites to issue electronic and physical receipts: Invoices, ND, NC, withholdings, Liq. Purchase, Purchase / sale receipts

Reference:
 https://www.srienlinea.gob.ec
    """,

    'author': "OpenAlliance Cía. Ltda",
    'website': "http://www.openalliance-la.com",
    'category': 'Technical',
    'version': '15.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'l10n_latam_base', 'l10n_latam_invoice_document', 'oa_base'],

    # always loaded
    "data": [
        'data/account_chart_template_ec.xml',
        'data/account_fiscal_position_template_ec.xml',
        'data/account_fiscal_position_ec.xml',
        'data/l10n_latam_identification_type_ec.xml',
        'data/l10n_latam.document.type_ec.xml',
        'data/res_bank_ec.xml',
      #  'data/res_partner_ec.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/views.xml',
        'views/l10n_latam_identification_type_views.xml',
        'views/account_move_views.xml',
        'security/ir.model.access.csv'
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
