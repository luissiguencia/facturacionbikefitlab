# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api, _

DEF_COMMENT = '''Dirección: ${cliente.street or ''}\nTelf: ${cliente.phone or cliente.mobile or ''}\nEmail: ${cliente.email or cliente.evoucher_notification_emails or ''}'''


class EvoucherEnvironment(models.Model):
    """Evoucher environment"""
    _name = 'oa.evoucher.environment'
    _description = 'E-voucher Environment'
    _order = 'sri_code asc'

    name = fields.Char(size=50, required=True, help="the name of this environment")
    sri_code = fields.Integer(copy=False, required=True, help="SRI code for this environment")
    reception_ws = fields.Char(copy=False, size=200, required=True, help="this field specify the SRI reception service for digital documents")
    authorization_ws = fields.Char(copy=False, size=200, required=True, help="this field specify the SRI authorization service for digital documents")
    evoucher_general_sequence = fields.Many2one('ir.sequence', required=True, help="the SRI evoucher related seqcuence used in generation of access keys")    
    # auth_time_waiting = fields.Integer(string='Authorization Wait Time', copy=False, help="this field specify the time waiting(in minutes) to request authorization service in offline auth method")
    # evoucher_auth_method = fields.Selection([('online', 'Online') ('offline', 'Offline') ], 'Auth. Method', required=True, help="the type of this environment")
    # max_filesize = fields.Integer('Reception max file size (Kb)', required=True, help="specify the max file size to get an response from reception WS")
    # evoucher_sign_method_id = fields.Many2one('oa.digital.signature.method', 'Evoucher sign service', required=True, help='this field is used to specify the digital signature method used with evoucher')
    # contingency_file = fields.Binary('SRI Contingency File')
    # contingency_key_ids = fields.One2many('oa.account.evoucher.sri.contingency.key', 'environment_id', 'Contingency Keys', help="this is used to contingency cases use.")

    _sql_constraints = [
        ('unique_environment', 'unique(name,sri_code)', 'The environment already exists'),
    ]


class EvoucherIssuerCertificate(models.Model):
    """Issuer Certificate"""
    _name = 'oa.evoucher.issuer.certificate'
    _description = 'Issuer Certificate'
    _order = 'not_valid_before'

    @api.depends('not_valid_after')
    def _compute_state(self):
        for record in self:
            record.state = 'Pending'
            if record.not_valid_after:
                if record.not_valid_after and record.not_valid_after.strftime('%Y-%m-%d') < time.strftime('%Y-%m-%d'):
                    record.state = 'Expired'
                else:
                    record.state = 'Active'

    issuer_id = fields.Many2one('oa.evoucher.issuer', required=True, help="the issuer")
    in_use = fields.Boolean(help="check this field if you want to use this certificate")
    certificate = fields.Binary(required=True, help="the certified p12 file used to sign the documents")
    password = fields.Char(size=124, required=True, help="the password used to open the p12 certificate")
    signer = fields.Char(size=124, required=True, help="the signer of the certificate")
    not_valid_before = fields.Date(required=True, help="the expiration date of the certificate")
    not_valid_after = fields.Date(required=True, help="the expiration date of the certificate")
    state = fields.Selection([('Pending', 'Pending'), ('Active', 'Active'), ('Expired', 'Expired')], required=True, default='Pending', compute=_compute_state, help="the state of the certificate related to this issuer")
    issuer = fields.Char(string='Issuer Name', size=256, required=True, help="the name of the certified entity")

    _sql_constraints = [
        ('unique_cert', 'unique(issuer_id,signer,not_valid_after,issuer)', 'The certificate already exists'),
    ]


class EvoucherIssuer(models.Model):
    """Document Issuer"""
    _name = 'oa.evoucher.issuer'
    _description = 'E-voucher Issuer'
    _order = 'name'

    def name_get(self):
        result = []
        for issuer in self:
            result.append((issuer.id, issuer.name + " (" + issuer.state + ")"))
        return result

    @api.depends('certificate_ids')
    def _compute_state(self):
        for record in self:
            record.state = 'Pending'
            for cert in record.certificate_ids:
                record.state = 'Pending'
                if cert.not_valid_after:
                    if cert.not_valid_after and cert.not_valid_after.strftime('%Y-%m-%d') < time.strftime('%Y-%m-%d'):
                        record.state = 'Expired'
                    else:
                        record.state = 'Active'

    name = fields.Char(size=50, required=True, help="the name of this person")
    state = fields.Selection([('Pending', 'Pending'), ('Active', 'Active'), ('Expired', 'Expired')], required=True, default='Pending', compute=_compute_state, help="the state of the certificate related to this issuer")
    certificate_ids = fields.One2many('oa.evoucher.issuer.certificate', 'issuer_id', string='Certificates', help="the certificates used by this user to generate de digital signature of documents")

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The environment already exists'),
    ]

    def add_cert(self):
        '''Add new certificate to this issuer
        '''
        record = self.env['oa.evoucher.add.cert.wizard'].create({'issuer_id': self.id, 'state': 'Pending'})  # pylint: disable=no-member
        return {
            'res_id': record.id,
            'name': _('Add certificate'),
            'view_mode': 'form',
            'res_model': 'oa.evoucher.add.cert.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class EvoucherLog(models.Model):
    """Object to store the log operations between system and SRI WS"""

    _name = 'oa.evoucher.log'
    _description = 'Object to store the log operations between system and SRI WS'

    # Fields
    move_id = fields.Many2one('account.move', 'Related Invoice')
    user_id = fields.Many2one('res.users', string='User', required=True, help="the related user to this operation")
    # retention_id: fields.Many2one('oa.account.sri.invoiceretention', 'Retention')
    # refguide_id: fields.Many2one('oa.account.sri.referenceguide', 'Ref. Guide')
    # liqcomp_id: fields.Many2one('account.invoice', 'Buy Liquidation')
    event = fields.Selection([('init', 'Initialization'), ('generate_xml', 'Generate Xml'), ('sign_xml', 'Sign Xml'), ('test_net', 'Testing Network'),
                              ('send_sri', 'Send SRI'), ('auth_sri', 'Auth SRI'), ('notified', 'Auth. and Notified'), ('annulled', 'Annulled')], required=True, help="the event related")
    answer = fields.Text(required=True, help="the answer for the event related")
    time = fields.Datetime(required=True, help="this is the time of the event")
    comment = fields.Text()

    _sql_constraints = [
        ('unique_invoice_event', 'unique(move_id,event,time,comment)', 'The event is duplicated for this docuemnt'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'user_id' not in vals:
                vals['user_id'] = self.env.uid
        return super().create(vals_list)


class EvoucherDocumentTemplate(models.Model):
    """Document Template used to generate the xml of the document to send to the SRI WS"""
    _name = 'oa.evoucher.document.template'
    _description = 'Document Template used to generate the xml of the document to send to the SRI WS'
    _rec_name = 'version'

    # Fields
    document_type_id = fields.Many2one('l10n_latam.document.type',  required=True, help='the document type related to this template',)
    active = fields.Boolean(help='check this field to active this template')
    version = fields.Char(size=10, required=True, help='the version of the tenplate')
    template_xml = fields.Text(required=True, help="the default comments for this template")

    _sql_constraints = [
        ("unique_template", "unique(document_type_id,version)", "The template already exists!"),
    ]
