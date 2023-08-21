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
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from operator import itemgetter
from odoo.tools import date_utils, groupby as groupbyelem
import base64


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
        religion_list = list(religion.keys())

        gender = dict(request.env['housemaid.maids'].fields_get(
            allfields=['gender'])['gender']['selection'])
        gender_list = list(gender.keys())

        marital_status = dict(request.env['housemaid.maids'].fields_get(
            allfields=['marital_status'])['marital_status']['selection'])
        marital_status_list = list(marital_status.keys())

        new_maid_url = '/my/maid/new'

        vals = {
            'default_url': new_maid_url,
            'user': curr_user,
            'offices': offices,
            'jobs': jobs,
            'country': country,
            'currency': currency,
            'education': education,
            'religion': religion_list,
            'gender': gender_list,
            'marital_status': marital_status_list,
            'page_name': 'my_maids_portal_new_form_view',
        }

        if request.httprequest.method == "POST":
            print("post....")
            print(kw)
            maid_vals = {}
            error_list = []

            if not kw.get('user'):
                error_list.append('User is mandatory.')
            if not kw.get('offices'):
                error_list.append('Office is mandatory.')
            if not kw.get('code'):
                error_list.append('Code is mandatory.')
            if not kw.get('name'):
                error_list.append('Name is mandatory.')
            if not kw.get('country'):
                error_list.append('Country is mandatory.')
            if not kw.get('jobs'):
                error_list.append('Job is mandatory.')
            if not kw.get('salary'):
                error_list.append('Monthly Salary is mandatory.')
            if not kw.get('currency'):
                error_list.append('Currency is mandatory.')
            if not kw.get('passport_no'):
                error_list.append('Passport No is mandatory.')
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
                error_list.append('Birthday is mandatory.')
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
                'currency_id': kw.get('currency'),
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

        return request.render(
            'ms_housemaid.my_maids_portal_new_form_view',
            vals,
        )

    @http.route(['/my/maids', '/my/maids/page/<int:page>'], type="http", website=True, auth='user')
    def my_maids_list_view(self, page=1, sortby=None, groupby=None, search="", search_in="all", **kw):
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

        searchbar_sortings = {
            'ida': {'label': 'ID Asc', 'order': 'id asc'},
            'idd': {'label': 'ID Desc', 'order': 'id desc'},
            'name': {'label': 'Name', 'order': 'name'},
            'country_id': {'label': 'Country', 'order': 'country_id'},
            'state': {'label': 'State', 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'ida'
        order = searchbar_sortings[sortby]['order']

        searchbar_groupby = {
            'None': {'input': 'None', 'label': _('None')},
            'jobs_id': {'input': 'jobs_id', 'label': _('Jobs')},
            'state': {'input': 'state', 'label': _('State')},
            'country_id': {'input': 'country_id', 'label': _('Country')},
        }
        maids_group_by = searchbar_groupby.get(groupby, {})
        if groupby in ('jobs_id', 'state', 'country_id'):
            maids_group_by = searchbar_groupby.get('input')
            order = maids_group_by+','+order
        else:
            maids_group_by = ''

        searchbar_inputs = {
            'all': {'label': 'All', 'input': 'all', 'domain': []},
            'name': {'label': 'Name', 'input': 'name', 'domain': [('name'), 'ilike', search]},
            'state': {'label': 'State', 'input': 'state', 'domain': [('state'), 'ilike', search]},
            'job': {'label': 'Job', 'input': 'job_id', 'domain': [('job_id.name'), 'ilike', search]},
        }
        # default groupby
        if not groupby:
            groupby = 'None'

        search_domain = searchbar_inputs[search_in]['domain']

        if search_domain:
            maids_domain.append(search_domain)

        total_maids = request.env['housemaid.maids'].sudo(
        ).search_count(maids_domain)

        maid_url = '/my/maids/'
        print('total = ', total_maids)
        pager_detail = pager(
            url=maid_url,
            url_args={'sortby': sortby, 'groupby': groupby,
                      'search_in': search_in, 'search': search},
            total=total_maids,
            page=page,
            step=10,
        )
        print('pager_detail = ', pager_detail)
        maids_obj = request.env['housemaid.maids']
        maids = request.env['housemaid.maids'].sudo().search(
            maids_domain,
            limit=10,
            order=order,
            offset=pager_detail['offset'],
        )
        # start groupby afte maids search
        if maids_group_by:
            maids_group_list = [{maids_group_by: k, 'maids': maids_obj.concat(
                *g)} for k, g in groupbyelem(maids, itemgetter(maids_group_by))]

        else:
            maids_group_list = [{'maids': maids}]

        print('maids = ', maids)
        vals = {
            'default_url': maid_url,
            'maids': maids,
            'page_name': 'my_maids_portal_list_view',
            'pager': pager_detail,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'search': search,
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
        vals = {
            'maids': maids_id,
            'page_name': 'my_maids_portal_form_view'
        }
        maids_rec = request.env['housemaid.maids'].sudo().search(maids_domain)
        maids_ids = maids_rec.ids
        maids_index = maids_ids.index(maids_id.id)
        if maids_index != 0 and maids_ids[maids_index - 1]:
            vals['prev_record'] = '/my/maids/{}'.format(
                maids_ids[maids_index-1])
        if maids_index < len(maids_ids) - 1 and maids_ids[maids_index + 1]:
            vals['next_record'] = '/my/maids/{}'.format(
                maids_ids[maids_index+1])

        return request.render("ms_housemaid.my_maids_portal_form_view", vals)

    @http.route(['/my/maids/print/<model("housemaid.maids"):maids_id>'], website=True, auth='user', type="http")
    def my_maids_report_print(self, maids_id, **kw):
        return self._show_report(model=maids_id, report_type='pdf', download=True,
                                 report_ref='ms_housemaid.action_report_action_maid_resume')

    @http.route('/my/maids/download_document/<model("housemaid.maids"):maids_id>', website=True, type='http', auth="user")
    @serialize_exception
    def download_document(self, maids_id, filename=None, **kw):
        """ Download link for files stored as binary fields.
        :param str model: name of the model to fetch the binary from
        :param str field: binary field
        :param str id: id of the record from which to fetch the binary
        :param str filename: field holding the file's name, if any
        :returns: :class:`werkzeug.wrappers.Response`
        """
        print(maids_id)
        binary_file = maids_id.resume
        filename = maids_id.resume_name
        filecontent = base64.b64decode(binary_file or '')
        content_type, disposition_content = False, False

        if not filecontent:
            return request.not_found()
        else:
            if not filename:
                filename = '%s_%s' % (
                    maids_id._name.replace('.', '_'), maids_id.id)
            content_type = ('Content-Type', 'application/octet-stream')
            disposition_content = ('Content-Disposition',
                                   content_disposition(filename))

        return request.make_response(filecontent, [content_type,
                                                   disposition_content])

    # Este es la funcion que debes agregar a tu clase
    def download(self):
        path = "/my/maids/download_document?"
        model = "housemaid.maids"
        filename = "Resume of "

        # esta es la funcion que genera mi archivo y lo almacena en el campo binario
        self.print_report()
        url = path + "model={}&id={}&filename={}.xls".format(
            model, self.id, filename)

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'tag': 'reload',
        }
