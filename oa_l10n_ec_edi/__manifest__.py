# -*- coding: utf-8 -*-
{
    'name': "Electronic Invoicing Ecuador(SRI)",

    'summary': """
        Ecuadorian Electronic Invoicing Module""",

    'description': """
        Module that enables the generation and reception of electronic documents managed by SRI (Internal Revenue Service) According to the technical sheets issued by the entity. They can be managed:
        - Bills
        - Credit notes
        - Debit Notes
        - Withholdings
        - Reference guides 
            """,

    'author': "OpenAlliance Cia. Ltda.",
    'website': "http://www.openalliance-la.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '15.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_edi', 'oa_l10n_ec'],

    # always loaded
    'data': [
        'security/security.xml',
        'data/sequence.xml',
        'data/environment.xml',
        'data/evoucher_template.xml',
        'data/l10n_latam_document_type_ec.xml',
        'views/res_company_views.xml',
        'views/evoucher_views.xml',
        'views/account_move_views.xml',
        'views/l10n_latam_document_type_views.xml',
        'wizard/oa_evoucher_add_cert_wizard_view.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "external_dependencies": {
        'python': ['cryptography', 'suds']
    },
}
