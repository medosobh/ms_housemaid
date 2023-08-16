# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal


class maidsportal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        rtn = super(maidsportal, self)._prepare_home_portal_values(counters)
        rtn['maids_count'] = request.env['housemaid.maids'].search_count([])
        return rtn

    @http.route(['/my/maids'], website=True, auth='user', type="http")
    def my_maids_list_view(self, **kw):
        maids = request.env['housemaid.maids'].sudo().search([])
        return request.render("ms_housemaid.my_maids_portal_list_view", {
            'maids': maids,
            'page_name': 'my_maids_portal_list_view'
        })

    @http.route(['/my/maids/<model("housemaid.maids"):maids_id>'], website=True, auth='user', type="http")
    def my_maids_form_view(self, maids_id, **kw):
        vals = {'maid':maids_id}
        return request.render("ms_housemaid.my_maids_portal_form_view",{
            vals
        })


class createmaids(http.Controller):
    @http.route('/maidform', website=True, auth='user', type="http")
    def maid_form(self, **kw):
        offices = request.env['housemaid.offices'].sudo().search([])
        print("open form")
        return request.render('ms_housemaid.maid_form', {
            'offices': offices
        })

    @http.route('/create/maid', website=True, auth='user', type="http")
    def create_maid(self, **kw):
        print("save form")
        request.env['housemaid.maids'].sudo().create(kw)
        return request.render('ms_housemaid.create_success', {})
