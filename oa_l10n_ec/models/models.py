# -*- coding: utf-8 -*-
"""Minimum tax prerequisites to issue electronic and physical receipts: Invoices, ND, NC, withholdings, Liq. Purchase, Purchase / sale receipts"""
from odoo import fields, models  # , api  # , SUPERUSER_ID, _


class OaBranchoffice(models.Model):
    """the branches or authorized establishments of the company according to the Ecuadorian regulation of the SRI """
    _name = 'oa.branchoffice'
    _description = 'the branches or authorized establishments of the company according to the Ecuadorian regulation of the SRI '
    _order = 'company_id asc'
    _date_name = 'activity_start_date'

    # Fields
    company_id = fields.Many2one('res.company', required=True, help='The company related to this branchoffice')
    serie = fields.Char(size=3, required=True, help='entity series number according to SRI regulations ')
    name = fields.Char(size=256, required=True, help='the name of the branchoffice also known as reference')
    address = fields.Char(size=256, required=True, help='the addess of the brachoffice')
    activity_start_date = fields.Date(required=True, help='the branchoffice activity start date ')
    emission_point_config_ids = fields.One2many('oa.emission.point.config', 'branchoffice_id', string='Emission Points')

    _sql_constraints = [
        ('unique_company_serie', 'unique(company_id,serie)', "the value of the field serie must be unique!"),
    ]

    def name_get(self):
        result = []
        for branchoffice in self:
            result.append((branchoffice.id, "(" + branchoffice.serie + ") " + branchoffice.name))
        return result


class OaEmissionPointConfig(models.Model):
    """object that allows setting the configuration of an issue point related to your accounting journal and the users"""
    _name = 'oa.emission.point.config'
    _description = 'object that allows setting the configuration of an issue point related to your accounting journal and the users'
    _order = 'name asc'

    # Fields
    name = fields.Char(required=True, help='the name of the emission point')
    branchoffice_id = fields.Many2one('oa.branchoffice', required=True, ondelete='cascade', help='the related branchoffice')
    serie = fields.Char(size=3, required=True, help='the emission point serie number')
    emission_type = fields.Selection([('internal', 'Internal'), ('external', 'External')], required=True, help='the type of the emission point')
    journal_id = fields.Many2one('account.journal', required=True, help='the account journal related to this emission point')
    doctype_id = fields.Many2one('l10n_latam.document.type', required=True, help='The type of document related to this emission point configuration')
    user_ids = fields.Many2many('res.users', 'oa_emission_point_res_users_rel', 'emission_point_config_id', 'user_id', help='the users related to this emission point config')

    _sql_constraints = [
        ('unique_branchoffice_serie', 'unique(branchoffice_id,serie)', "the value of the field serie must be unique!"),
    ]

    def name_get(self):
        result = []
        for point in self:
            result.append((point.id, "(" + point.serie + ") " + point.name))
        return result
