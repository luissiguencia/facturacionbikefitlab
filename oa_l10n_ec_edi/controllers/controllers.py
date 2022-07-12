# -*- coding: utf-8 -*-
# from odoo import http


# class Evoucher(http.Controller):
#     @http.route('/evoucher/evoucher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/evoucher/evoucher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('evoucher.listing', {
#             'root': '/evoucher/evoucher',
#             'objects': http.request.env['evoucher.evoucher'].search([]),
#         })

#     @http.route('/evoucher/evoucher/objects/<model("evoucher.evoucher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('evoucher.object', {
#             'object': obj
#         })
