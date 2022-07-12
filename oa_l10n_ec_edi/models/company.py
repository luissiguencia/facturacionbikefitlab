# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    """Inherit REs company"""

    _inherit = "res.company"

    # Columns
    evoucher_enable = fields.Boolean(string='Enable e-voucher', default=True, help='this field is used to enable or disable the capability of this company to generate SRI e-voucher')
    evoucher_environment = fields.Many2one('oa.evoucher.environment', string='Environment', help='this field is used to specify the digital signature method used with e-voucher')
    # evoucher_offline_delay = fields.Integer(string='Authorization Delay', default=24, help="use this field to specify the waiting time between receipt and voucher authorization in the offline schema")
    evoucher_issuer = fields.Many2one('oa.evoucher.issuer', string='Issuer', help="The default person who signs the electronic vouchers for the company")
    evoucher_sender_email = fields.Char(string='Sender Email', help="use this field to specify the default email sender for the e-voucher email notification")
    evoucher_emission_method = fields.Selection([('Online', 'Online'), ('Schedule', 'Scheduled')], default='Schedule', string='Issue Method', required=True, help='this field is used to enable or disable the capability of this company to generate SRI evoucher this option might be overwrited by emission poin configuration')
    evoucher_send_time = fields.Float(string='Send time', help="this field specify the hour and minute when the e-vouchers in queued state are sent to the SRI WS", default=22)
