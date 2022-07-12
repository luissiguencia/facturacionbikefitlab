# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class L10nLatamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"

    internal_type = fields.Selection(selection_add=[('retention', 'Retention'), ('purchase_liquidation', 'Purchase Liquidation')])
