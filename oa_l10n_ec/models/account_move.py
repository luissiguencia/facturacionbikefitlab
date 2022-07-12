# -*- coding: utf-8 -*-
"""Account move redefinition"""
from odoo import fields, models  # , api  # , SUPERUSER_ID, _


class AccountMove(models.Model):
    """Inherit from account move"""
    _inherit = 'account.move'

    # Fields
    branchoffice_id = fields.Many2one('oa.branchoffice', help='the emission point config used to issue this invoice')
    emission_point_config_id = fields.Many2one('oa.emission.point.config', string='Emission Point', help='the emission point config used to issue this invoice')


class ResCompany(models.Model):
    """Inherit from res.company"""
    _inherit = 'res.company'

    # Fields
    mandatory_accounting = fields.Boolean(help='this field indicates if the company is required to keep accounts with the SRI')
    special_tax_payer_code = fields.Char(size=15, help='this field indicates if the company is a SRI special tax payer')
    retention_agent = fields.Boolean(help='this field indicates if the company is retention agent according to the SRI')
    branch_ids = fields.One2many('oa.branchoffice', 'company_id', help='the branches or authorized establishments of the company according to the Ecuadorian regulation of the SRI ')
