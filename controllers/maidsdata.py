# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import fields, http, _
from odoo.http import request
from odoo.fields import Command
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.exceptions import UserError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class maidsportal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(maidsportal, self)._prepare_home_portal_values(counters)
        user_id = request.env.uid
        curr_user = request.env['res.users'].search([
            ('id', '=', user_id),
        ],
            limit=1
        )
        user_office = curr_user.offices_id.id

        maids_domain = [
            ('user_id', '=', user_id),
            ('offices_id', '=', user_office),
        ]
        values['maids_count'] = request.env['housemaid.maids'].search_count(
            maids_domain)
        return values

    @http.route('/my/maid/new', website=True, auth='user', type="http", method=["POST", "GET"])
    def maid_create_form(self, **kw):
        vals = super()._prepare_portal_layout_values()
        user_id = request.env.uid
        curr_user = request.env['res.users'].search([
            ('id', '=', user_id),
        ],
            limit=1
        )
        user_office = curr_user.offices_id.id
        domain = [
            ('id', '=', user_office),
        ]

        offices = request.env['housemaid.offices'].sudo().search(
            domain, limit=1)
        jobs = request.env['housemaid.jobs'].sudo().search([])
        # country = request.env['res.country'].sudo().search([])
        country = offices.country_id
        currency = request.env['res.currency'].sudo().search([])
        education = request.env['housemaid.educations'].sudo().search([])

        religion = dict(request.env['housemaid.maids'].fields_get(
            allfields=['religion'])['religion']['selection'])
        print(religion)
        print(len(religion))

        gender = dict(request.env['housemaid.maids'].fields_get(
            allfields=['gender'])['gender']['selection'])
        print(gender)
        print(len(gender))

        new_maid_url = '/my/maid/new'

        error_list = []
        maid_vals = {}
        if not kw.get('user'):
            error_list.append('User is mandatory.')
        if not kw.get('offices'):
            error_list.append('Office is mandatory.')
        if not kw.get('code'):
            error_list.append('Code is mandatory.')
        if not kw.get('name'):
            error_list.append('Name is mandatory.')
        if not kw.get('jobs'):
            error_list.append('Job is mandatory.')
        if not kw.get('salary'):
            error_list.append('Monthly Salary is mandatory.')
        if not kw.get('currency'):
            error_list.append('Currency is mandatory.')

        if request.httprequest.method == "POST":
            print("post....")
            print(kw)
            passport_issue_date = len(kw.get('passport_issue_date'))
            if not passport_issue_date:
                passport_issue_date = None
            else:
                passport_issue_date = kw.get('passport_issue_date')

            passport_expire_date = len(kw.get('passport_expire_date'))
            if not passport_expire_date:
                passport_expire_date = None
            else:
                passport_expire_date = kw.get('passport_expire_date')

            birthday = len(kw.get('birthday'))
            if not birthday:
                birthday = None
            else:
                birthday = kw.get('birthday')

            maid_vals = {
                'user_id': kw.get('user'),
                'offices_id': kw.get('offices'),
                'code': kw.get('code'),
                'name': kw.get('name'),
                'phone': kw.get('phone'),
                'email': kw.get('email'),
                'country_id': kw.get('country'),
                'jobs_id': kw.get('jobs'),
                'monthly_salary': kw.get('salary'),
                'currency_id': int(kw.get('currency')),
                'contract_period': kw.get('period'),
                'arabic_lang': kw.get('arabic'),
                'english_lang': kw.get('english'),
                'educations_id': kw.get('education'),
                'passport_no': kw.get('passport_no'),
                'passport_place': kw.get('passport_place'),
                'passport_issue_date': passport_issue_date,
                'passport_expire_date': passport_expire_date,
                'identation': kw.get('identation'),
                'religion': kw.get('religion'),
                'gender': kw.get('gender'),
                'children_no': kw.get('children_no'),
                'birthday': birthday,
                'place_of_birth': kw.get('place_of_birth'),
                'marital_status': kw.get('marital_status'),
                'skin_color': kw.get('skin_color'),
                'hight': kw.get('hight'),
                'weight': kw.get('weight'),
                'skills_cleaning': kw.get('skills_cleaning'),
                'skills_arabic_cooking': kw.get('skills_arabic_cooking'),
                'skills_baby_sitting': kw.get('skills_baby_sitting'),
                'skills_washing': kw.get('skills_washing'),
                'skills_ironing': kw.get('skills_ironing'),
                'skills_googlelocation': kw.get('skills_googlelocation'),
                'skills_driving': kw.get('skills_driving'),
            }
            print(error_list)
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
            'user': curr_user,
            'offices': offices,
            'jobs': jobs,
            'country': country,
            'currency': currency,
            'education': education,
            'page_name': 'my_maids_portal_new_form_view',
            # 'success_msg':success_msg,
            # 'error_list': error_list,
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
            'state': {'label': 'State', 'order': 'state'},
        }
        searchbar_groupby = {
            'None': {'input': 'None', 'label': _('None')},
            'country_id': {'input': 'country_id', 'label': _('Country')},
            'jobs_id': {'input': 'jobs_id', 'label': _('Jobs')},
            'state': {'input': 'state', 'label': _('State')},
        }

        user_id = request.env.uid
        curr_user = request.env['res.users'].search([
            ('id', '=', user_id),
        ],
            limit=1
        )
        user_office = curr_user.offices_id.id
        maids_domain = [
            ('user_id', '=', user_id),
            ('offices_id', '=', user_office),
        ]
        # default sort by order
        if not sortby:
            sortby = 'id'
        order = searchbar_sortings[sortby]['order']
        # default groupby
        if not groupby:
            groupby = 'None'

        total_maids = request.env['housemaid.maids'].sudo(
        ).search_count(maids_domain)

        maid_url = '/my/maids'
        pager = portal_pager(
            url=maid_url,
            url_args={'sortby': sortby, 'groupby': groupby},
            total=total_maids,
            page=page,
            step=10,
        )
        maids = request.env['housemaid.maids'].sudo().search(
            maids_domain,
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

        user_id = request.env.uid
        curr_user = request.env['res.users'].search([
            ('id', '=', user_id),
        ],
            limit=1
        )
        user_office = curr_user.offices_id.id
        maids_domain = [
            ('user_id', '=', user_id),
            ('offices_id', '=', user_office),
        ]

        maids_rec = request.env['housemaid.maids'].sudo().search(maids_domain)
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
