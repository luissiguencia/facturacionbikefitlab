"""Cert wizard"""
import time
import base64
import logging
from odoo import fields, api, models
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)
try:
    import cryptography.hazmat.primitives.serialization.pkcs12 as pk
except ImportError:
    _logger.warning("Can ton find cryptography module")


class AddCertWizard(models.TransientModel):
    """Wizard to add p12 cert"""
    _name = 'oa.evoucher.add.cert.wizard'
    _description = 'Wizard to add p12 cert to sign xml files'
    rec_naeme = 'issuer_id'

    @api.depends('not_valid_after')
    def _compute_state(self):
        for record in self:
            record.state = 'Pending'
            if record.not_valid_after:
                if record.not_valid_after and record.not_valid_after.strftime('%Y-%m-%d') < time.strftime('%Y-%m-%d'):
                    record.state = 'Expired'
                else:
                    record.state = 'Active'

    # Fields
    issuer_id = fields.Many2one('oa.evoucher.issuer', required=True, help="the issuer of this certificate")
    certificate = fields.Binary(help="the certified p12 file used to sign the documents")
    password = fields.Char(size=124, help="the password used to open the p12 certificate")
    signer = fields.Char(size=124, help="the signer of the certificate")
    not_valid_before = fields.Date(help="the expiration date of the certificate")
    not_valid_after = fields.Date(help="the expiration date of the certificate")
    issuer_name = fields.Char(size=256, help="the name of the certified entity")
    signer_aux = fields.Char(size=124, help="the signer of the certificate")
    not_valid_before_aux = fields.Date(string="Not valid before", help="the expiration date of the certificate")
    not_valid_after_aux = fields.Date(string="Not valid after", help="the expiration date of the certificate")
    issuer_aux = fields.Char(size=256, help="the name of the certified entity")
    state = fields.Selection([('Pending', 'Pending'), ('Active', 'Active'), ('Expired', 'Expired')], required=True, default='Pending', compute=_compute_state, help="the state of the certificate related to this issuer")

    @api.onchange('certificate', 'password')
    def _onchange_password(self):
        if self.password and self.certificate:
            try:
                issuername = False
                p12 = pk.load_key_and_certificates(base64.b64decode(self.certificate), str.encode(self.password))
                for item in p12:
                    if type(item).__name__ == 'Certificate':
                        certificate = item
                        issuername = certificate.issuer.rfc4514_string()
                        subject = certificate.subject
                        for att in subject._attributes:
                            if att.rfc4514_string()[:2] == 'CN':
                                signername = att.rfc4514_string()[3:]
                                if '+' in signername:
                                    signername = signername.spli('+')[0]
                                break
                        not_valid_after = certificate.not_valid_after
                        not_valid_before = certificate.not_valid_before
                if not signername:
                    return {
                        'warning': {'title': "Error", 'message': "No Signer found in database"},
                    }
                self.signer = signername
                self.signer_aux = signername
                self.issuer_name = issuername
                self.issuer_aux = issuername
                self.not_valid_after = not_valid_after.strftime('%Y-%m-%d')
                self.not_valid_after_aux = not_valid_after.strftime('%Y-%m-%d')
                self.not_valid_before = not_valid_before.strftime('%Y-%m-%d')
                self.not_valid_before_aux = not_valid_before.strftime('%Y-%m-%d')
                if not_valid_before.strftime('%Y-%m-%d') < time.strftime('%Y-%m-%d') <= not_valid_after.strftime('%Y-%m-%d'):
                    self.state = 'Active'
                else:
                    self.state = 'Expired'
            except ValidationError:
                return {
                    'warning': {'title': "Error", 'message': "The password and certificate doesn't match", 'type': 'notification'},
                }

    def save_cert(self):
        """Method to store a new cert
        Returns:
            True
        """
        self.env['oa.evoucher.issuer.certificate'].create({'in_use': True, 'issuer_id': self.issuer_id.id, 'certificate': self.certificate, 'password': self.password, 'issuer': self.issuer_name, 'signer': self.signer, 'not_valid_after': self.not_valid_after, 'not_valid_before': self.not_valid_before})
        return True
