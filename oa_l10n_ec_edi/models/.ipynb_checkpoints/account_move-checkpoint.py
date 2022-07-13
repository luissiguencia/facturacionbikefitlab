"""Evoucher implementatiion for invoice(account move)"""

import logging
import os
from odoo.modules import get_module_path
from odoo import fields, models, api
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    """Inherit from account move(Invoice)"""
    _inherit = 'account.move'

    evoucher_state = fields.Selection([('draft', 'Draft'), ('init', 'Init'), ('denied', 'Denied by Configuration'), ('queued', 'Queued'),
                                      ('xml_ready', 'XML READY'), ('signed', 'Signed'), ('ready', 'Ready to send'), ('sended', 'Sended to SRI'),
                                      ('received', 'Received'), ('returned', 'Returned From SRI'), ('authorized', 'Authorized From SRI'), ('rejected', 'Rejected'),
                                      ('contingency_ready', 'Contingency Ready'), ('notify_quenue', 'Notification Quenued'),
                                      ('annulled', 'Annulled'), ('not_apply', 'Not Apply'), ('not_authorized', 'Not Autorized')], default='draft', help='the evoucher state of the document')
    evoucher_enable = fields.Boolean()
    evoucher_file = fields.Binary()
    evoucher_auth_date = fields.Char(string='Auth Date', size=50, help="the date of the evoucher authorization")
    evoucher_rec_date = fields.Datetime(string='Received Date', help="the date of the evoucher reception")
    evoucher_notification_emails = fields.Char(string='Email to Notify', size=300, help="this are the emails used to send the evoucher when process is completed")
    evoucher_invlude_attachments = fields.Boolean(string='Include Atachments', help="include all atachments in the evoucher notification email: use this option when you want to add all the object attachments in the notification email send to the customer/provider")
    evoucher_access_key = fields.Char(string='Access Key', size=50, help="this field store the access key used to send file to SRI")
    evoucher_environment_id = fields.Many2one('oa.evoucher.environment', 'Environment', help="this is the environment used to generate this evoucher")
    evoucher_help_field = fields.Char(string='Help', size=100, help="please click the link to test service")
    evoucher_force_stop = fields.Boolean('Force stop evoucher process', help="check this field if you want to stop manually the evoucher process, the account process wil be executed normally")
    evoucher_notification_sent = fields.Boolean('Notification Sent?', help="this field indicates if the evoucher was notified to the client/supplier")
    evoucher_log = fields.One2many('oa.evoucher.log', 'move_id', help="this is the events log related to this evoucher process")
    # evoucher_authorization = fields.Char(string='Evoucher Auth', size=50, help="the authorization gived by the SRI"),
    # evoucher_emission = fields.Selection([('1', 'NORMAL'), ('2', 'INDISPONIBILIDAD')], 'Emission', help="the enviroment used to issue the evoucher"),
    # evoucher_auth_method = fields.related('environment_id', 'evoucher_auth_method', type='Selection', Selection=[('online', 'Online'), ('offline', 'Offline'), ], string='Auth Method'),
    # evoucher_batch_file = fields.Binary(),
    # evoucher_sequence = fields.Char('Secuence', size=15, help="this field store the secuence of the voucher used to generate access key before send file to SRI"),

    _sql_constraints = [
        ('unique_evoucher_access_key', 'unique(evoucher_access_key)', 'This access key is already registered and must be unique!'),
        # ('unique_evoucher_auth', 'unique(evoucher_authorization)', 'This authorization is already registered and must be unique!'),
    ]

    @api.model
    def run_evoucher_process(self):
        """Run evoucher process, control state and result of the process"""
        return True

    def test_sign(self):
        """Run evoucher process, control state and result of the process"""
        path = get_module_path('oa_l10n_ec_edi')
        res = os.system(f"java -Xmx120M -jar {path}/static/src/lib/xadesbes/XadesBes.jar {path}/test/test.xml  {path}/test/result.xml {path}/test/cert.p12 GECPfirma2021")
        return res
    
    def action_post(self):
        self.evoucher_state="queued"
        return super(AccountMove,self).action_post()
    
    def button_dratf(self):
        import pdb;pdb.set_trace()
        if self.evoucher_state=="queued":
            self.evoucher_state="dratf"
        return super(AccountMove,self).button_dratf()
            
    
    
 