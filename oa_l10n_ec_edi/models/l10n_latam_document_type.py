# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class L10nLatamDocumentType(models.Model):
    """l10n Document type"""
    _inherit = "l10n_latam.document.type"

    evoucher_enable = fields.Boolean(help='chck this field if you want to enable evoucher emission for this document')
    evoucher_template_ids = fields.One2many('oa.evoucher.document.template', 'document_type_id', required=True, help="this field is used to specify the vouchers tempates to send files to SRI WS")
