# -*- coding: utf-8 -*-
"""Minimum tax prerequisites to issue electronic and physical receipts: Invoices, ND, NC, withholdings, Liq. Purchase, Purchase / sale receipts"""
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from . import extras


class ResPartner(models.Model):
    """Inherit from res.partner"""
    _inherit = 'res.partner'

    # Fields
    same_name_partner_id = fields.Many2one('res.partner', string='Partner with same name', compute='_compute_same_name_partner_id', store=False)

    _sql_constraints = [
        ('unique_email', 'unique(email)', "the email of the partner must be unique!"),
    ]

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].upper()
        return super(ResPartner, self).write(vals)

    def _get_similarity_partner_name_ids(self):
        self._cr.execute("""
                SELECT id
                FROM res_partner
                WHERE SIMILARITY(name,%s) > 0.81;   
            """, (self.name,))
        similarity = self._cr.fetchall()
        similar_ids = []
        for similar in similarity:
            similar_ids.append(similar[0])
        return similar_ids

    @api.onchange('name')
    def _on_change_partner_name(self):
        if self.name:
            self.name = self.name.upper()
            similar_ids = self._get_similarity_partner_name_ids()
            if similar_ids:
                self.same_name_partner_id = similar_ids[0]

    @api.depends('name', 'company_id')
    def _compute_same_name_partner_id(self):
        for partner in self:
            partner_id = partner._origin.id
            ppartner = self.with_context(active_test=False).sudo()
            domain = [
                ('name', '=', partner.name),
                ('company_id', 'in', [False, partner.company_id.id]),
            ]
            if partner_id:
                domain += [('id', '!=', partner_id), '!', ('id', 'child_of', partner_id)]
            partner.same_name_partner_id = bool(partner.name) and not partner.parent_id and ppartner.search(domain, limit=1)

    @api.constrains('name')
    def _validate_name(self):
        for record in self:
            if record.name:
                if not extras.validate_partner_name(record.name):
                    raise ValidationError(_("The value entered for the partner name is incorrect, please make sure it is at least 5 characters long, does not contain special characters, is not an exclusively numeric name, etc."))
                if len(self.search([('name', '=', record.name)])) > 1:
                    raise ValidationError(_("There is another person with the same name in the system "))

    @api.constrains('email')
    def _validate_email(self):
        for record in self:
            if record.email:
                if not extras.validate_email_address(record.email):
                    raise ValidationError(_("The value entered for the email of the partner is incorrect or has an incorrect format, plase be shure than only address y specified and the address is valid!"))
