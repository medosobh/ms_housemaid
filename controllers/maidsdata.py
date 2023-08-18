# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class maidsportal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(maidsportal, self)._prepare_home_portal_values(counters)
        values['maids_count'] = request.env['housemaid.maids'].search_count([])
        return values
    
    @http.route('/my/maid/new', website=True, auth='user', type="http", method=["POST","GET"])
    def maid_create_form(self, **kw):
        vals = super()._prepare_portal_layout_values()
        offices = request.env['housemaid.offices'].sudo().search([])
        country = request.env['res.country'].sudo().search([])
        new_maid_url = '/my/maid/new'
        
        error_list = []
        maid_vals = {}
        if kw.get('office'):
            error_list.append('Name is mandatory.')
        else:
            maid_vals

        if request.httprequest.method == "POST":
            print("post....")
            maid_vals = {
                'offices_id': kw.get('offices'),
                'code': kw.get('code'),
                'name': kw.get('name'),
                'phone': kw.get('phone'),
                'email': kw.get('email'),
                'country_id': kw.get('country'),
                
            }
            if not error_list:
                request.env['housemaid.maids'].sudo().create(maid_vals)
                success_msg = 'Successfuly, New Maid Created'
                vals['success_msg'] = success_msg
            else:
                vals['error_list'] = error_list
        else:
            print("get....")


        vals = {
            'default_url': new_maid_url,
            'offices': offices,
            'country': country,
            'page_name': 'my_maids_portal_new_form_view',
        }

        return request.render(
            'ms_housemaid.my_maids_portal_new_form_view',
            vals,
        
        )

    

    @http.route(['/my/maids', '/my/maids/page/<int:page>'], type="http", website=True, auth='user')
    def my_maids_list_view(self, page=1, sortby=None, groupby=None, **kw):
        vals = super()._prepare_portal_layout_values()
        searchbar_sortings = {
            'id': {'label': 'ID Desc', 'order': 'id desc'},
            'name': {'label': 'Name', 'order': 'name'},
            'country_id': {'label': 'Country', 'order': 'country_id'},
        }
        searchbar_groupby = {
            'country_id': {'input': 'country_id', 'label': 'Country', 'order': 1},
            'jobs_id': {'input': 'jobs_id', 'label': 'Jobs', 'order': 1},
        }
        # default sort by order
        if not sortby:
            sortby = 'id'
        order = searchbar_sortings[sortby]['order']
        # default groupby
        if not groupby:
            groupby = 'None'

        total_maids = request.env['housemaid.maids'].sudo().search_count([])
        maid_url = '/my/maids'
        pager = portal_pager(
            url=maid_url,
            url_args={'sortby': sortby, 'groupby': groupby},
            total=total_maids,
            page=page,
            step=10,
        )
        maids = request.env['housemaid.maids'].sudo().search(
            [],
            limit=10,
            order=order,
            offset=pager['offset'],
        )
        vals = {
            'default_url': maid_url,
            'maids': maids,
            'page_name': 'my_maids_portal_list_view',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
        }

        return request.render(
            "ms_housemaid.my_maids_portal_list_view",
            vals,
        )

    @http.route(['/my/maids/<model("housemaid.maids"):maids_id>'], website=True, auth='user', type="http")
    def my_maids_form_view(self, maids_id, **kw):
        vals = super()._prepare_portal_layout_values()
        
        maids_rec = request.env['housemaid.maids'].sudo().search([])
        maids_ids = maids_rec.ids
        maids_index = maids_ids.index(maids_id.id)
        if maids_index != 0 and maids_ids[maids_index - 1]:
            vals['prev_record'] = format(
                maids_ids[maids_index-1])
        if maids_index < len(maids_ids) - 1 and maids_ids[maids_index + 1]:
            vals['next_record'] = format(
                maids_ids[maids_index+1])
            
        vals = {
            'maid': maids_id,
            'page_name': 'my_maids_portal_form_view'
        }    
        return request.render("ms_housemaid.my_maids_portal_form_view", vals)

    @http.route(['/my/maids/print/<model("housemaid.maids"):maids_id>'], website=True, auth='user', type="http")
    def my_maids_report_print(self, maids_id, **kw):
        vals = super()._prepare_portal_layout_values()
        return self._show_report(self, model=maids_id, report_type='pdf', report_ref='', download=True)
