from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class maidslogs(models.Model):
    _name = 'housemaid.maidslogs'
    _description = 'Maid Logs'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    issue_date = fields.Date(
        string='Issue Date',
        required=True,
        default=datetime.today(),
        tracking=True
    )
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=False,
        string='Ticket no.',
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Current Sponser',
        tracking=True,
    )
    maids_id = fields.Many2one(
        string='Maids',
        comodel_name='housemaid.maids',
        required=True,
        tracking=True,
    )
    offices_id = fields.Many2one(
        'housemaid.offices',
        string='Offices',
        related='maids_id.offices_id',
        required=True,
        tracking=True,
    )
    contract_no = fields.Char(
        string='Contract No.',
        required=True,
        tracking=True,
    )
    start_contract = fields.Date(
        string='Start Date',
        required=True,
        tracking=True,
    )
    end_contract = fields.Date(
        string='End Date',
        required=True,
        tracking=True,
    )
    visa_no = fields.Char(
        string='Visa No.',
        required=False,
        tracking=True
    )
    user_id = fields.Many2one(
        string="Responsable",
        comodel_name='res.users',
        required=True,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
