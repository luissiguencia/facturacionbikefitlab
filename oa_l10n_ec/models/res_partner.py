# -*- coding: utf-8 -*-
"""Minimum tax prerequisites to issue electronic and physical receipts: Invoices, ND, NC, withholdings, Liq. Purchase, Purchase / sale receipts"""
from odoo import models, api, _
from odoo.exceptions import ValidationError
from . import extras


class Partner(models.Model):
    """Inherit from res.partner"""
    _inherit = 'res.partner'

    # Fields

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return super(Partner, self)._address_fields() + ['phone','mobile','vat', 'l10n_latam_identification_type_id']

    '''@api.model
    def name_get(self):
        res = super(Partner,self).name_get()
        if self._context.get('show_vat'):
            res = []
            for partner in self:
                res.append((partner.id, partner.name + (partner.l10n_latam_identification_type_id and (" ("+partner.l10n_latam_identification_type_id.name + ':'+(partner.vat or '')+")"))))
        return res'''

    @api.model
    def default_get(self, fields_list):
        """Set CI by default identification_type in partner where individual is set as company_type
        """
        res = super(Partner, self).default_get(fields_list)
        if 'l10n_latam_identification_type_id' not in fields_list:
            if res.get('is_company'):
                identification_type = self.env.ref('oa_l10n_ec.identification_type_ruc')
                res['l10n_latam_identification_type_id'] = identification_type.id
            else:
                identification_type = self.env.ref('oa_l10n_ec.identification_type_cedula')
                res['l10n_latam_identification_type_id'] = identification_type.id
        return res

    @api.onchange('name', 'vat', 'l10n_latam_identification_type_id', 'property_account_position_id')
    def _on_change_partner_vals(self):
        if self.property_account_position_id:  # pylint: disable=no-member
            if 'Natural' in self.property_account_position_id.name:  # pylint: disable=no-member
                identification_type = self.env.ref('oa_l10n_ec.identification_type_cedula')
                self.l10n_latam_identification_type_id = identification_type.id
            else:
                identification_type = self.env.ref('oa_l10n_ec.identification_type_ruc')
                self.l10n_latam_identification_type_id = identification_type.id
        if self.vat and self.l10n_latam_identification_type_id and self.l10n_latam_identification_type_id.name in ['Cédula', 'RUC']:
            if not extras.validate_cedula_ruc(self.vat, self.l10n_latam_identification_type_id.name):
                self.vat = None
                self.l10n_latam_identification_type_id = None
                return {
                    'warning': {
                        'title': _("Warning!"),
                        'message': 'The entered value of the ID / RUC is incorrect or does not comply with the standard of the control bodies!'
                    }}

    @api.constrains('vat', 'l10n_latam_identification_type_id')
    def _validate_vat(self):
        for record in self:
            if record.vat and record.l10n_latam_identification_type_id:
                if record.l10n_latam_identification_type_id.name in ['Cédula', 'RUC']:
                    if not extras.validate_cedula_ruc(record.vat, record.l10n_latam_identification_type_id.name):
                        raise ValidationError(_("The entered value of the ID / RUC is incorrect or does not comply with the standard of the control bodies!"))
