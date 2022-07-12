# -*- coding: utf-8 -*-
{
    'name': "OpenAlliance Base Module",
    'summary': """
        Basic methods and controls implemented to the base objects in odoo in order to improve functionallity
        """,

    'description': """
OpenAlliance Base Module
============================================

Author: OpenAlliance Cía. Ltda.
        https://www.openalliance-la.com

   """,
    'author': "OpenAlliance Cía. Ltda",
    'website': "http://www.openalliance-la.com",
    'category': 'Technical',
    'version': '15.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    "data": [
        'views/res_partner_views.xml',
        'sql/pg_trgm.sql',
    ],
}
