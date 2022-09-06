# -*- coding: utf-8 -*-
# from odoo import http


# class Tem(http.Controller):
#     @http.route('/tem/tem', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tem/tem/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tem.listing', {
#             'root': '/tem/tem',
#             'objects': http.request.env['tem.tem'].search([]),
#         })

#     @http.route('/tem/tem/objects/<model("tem.tem"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tem.object', {
#             'object': obj
#         })
