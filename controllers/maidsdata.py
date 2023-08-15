# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError


class maids(http.Controller):
    @http.route('/mymaids/', website=True, auth='user', type="http")
    def housmaid_maids(self, **kw):
        # return "hello external office"        
        maids = request.env['housemaid.maids'].sudo().search([])
        return request.render("ms_housemaid.maids_page", {
            'maids': maids
        })
        
    @http.route('/maidform', website=True, auth='user', type="http")
    def maid_form(self, **kw):
        print("open form")
        maids = request.env['housemaid.maids'].sudo().search([])
        return request.render('ms_housemaid.maid_form',{
        })
    
    @http.route('/create/webmaid', website=True, auth='user', type="http")
    def maid_form(self, **kw):
        print("open form")
        request.env['housemaid.maids'].sudo().create(kw)
        return request.render('ms_housemaid.create_success',{})
