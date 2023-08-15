# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError, ValidationError


class maids(http.Controller):
    @http.route('/housemaid/maids/', website=True, auth='user')
    def housmaid_maids(self, **kw):
        # return "hello external office"
        return request.render("ms_housmaid.maids_page", {})