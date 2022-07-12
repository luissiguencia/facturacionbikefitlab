# from odoo import http


# class OaL10nEc(http.Controller):
#     @http.route('/oa_l10n_ec/oa_l10n_ec', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oa_l10n_ec/oa_l10n_ec/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('oa_l10n_ec.listing', {
#             'root': '/oa_l10n_ec/oa_l10n_ec',
#             'objects': http.request.env['oa_l10n_ec.oa_l10n_ec'].search([]),
#         })

#     @http.route('/oa_l10n_ec/oa_l10n_ec/objects/<model("oa_l10n_ec.oa_l10n_ec"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oa_l10n_ec.object', {
#             'object': obj
#         })
